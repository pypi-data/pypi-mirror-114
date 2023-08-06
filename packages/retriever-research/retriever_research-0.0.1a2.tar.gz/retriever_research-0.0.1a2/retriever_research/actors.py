import math
import queue
import sys
import threading
from typing import cast, Type, Dict
from types import TracebackType
import multiprocessing as mp
import boto3
import time
import json

import pykka

from retriever_research import messages
from retriever_research.config import Config


class FileListGeneratorActor(pykka.ThreadingActor):
    use_daemon_thread = True
    def __init__(self, file_chunker_ref, rate_limiter_ref: pykka.ActorRef, num_files_tracker_ref: pykka.ActorRef):
        kwargs = {"file_chunker_ref": file_chunker_ref}
        super().__init__(**kwargs)
        self.file_chunker_ref = file_chunker_ref
        self.rate_limiter_ref = rate_limiter_ref
        self.num_files_tracker_ref = num_files_tracker_ref

    def on_receive(self, msg):
        assert type(msg) == messages.RetrieveRequestMsg

        num_files = 0
        # Call S3 API to list objects within the prefix.
        s3_client = boto3.client('s3', region_name=msg.s3_region)
        paginator = s3_client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket=msg.s3_bucket,
            Prefix=msg.s3_prefix,
        )

        # TODO: Keep listing even if rate limiter is preventing us from sending DownloadRequest
        #       downstream. We want to know the total number of files ASAP.
        for resp in response_iterator:
            for file in resp["Contents"]:
                key = file["Key"]
                # etag = file["ETag"]
                size = file["Size"]
                while self.rate_limiter_ref.ask(messages.QueryWIP()) > Config.MAX_WIP:
                    # print(f"WIP {self.rate_limiter_ref.ask(messages.QueryWIP())}")
                    time.sleep(0.1)
                # print(f"Sending FileDownloadRequest {key}")
                self.file_chunker_ref.tell(messages.FileDownloadRequestMsg(
                    file_id=f"s3://{msg.s3_bucket}/{key}",
                    s3_bucket=msg.s3_bucket,
                    s3_key=key,
                    s3_region=msg.s3_region,
                    file_size=size
                ))
                num_files += 1
        self.num_files_tracker_ref.tell(messages.SetNumFiles(num_files=num_files))
        if num_files == 0:
            raise RuntimeError("No files match prefix")

    def on_stop(self) -> None:
        print("FileListGeneratorActor onstop")

class FileChunkerActor(pykka.ThreadingActor):
    use_daemon_thread = True
    CHUNK_SIZE_BYTES = 8_000_000

    def __init__(self, parallel_chunk_downloader_ref, rate_limiter_ref: pykka.ActorRef):
        kwargs = {"parallel_chunk_downloader_ref": parallel_chunk_downloader_ref}
        super().__init__(**kwargs)
        self.parallel_chunk_downloader_ref = parallel_chunk_downloader_ref
        self.rate_limiter_ref = rate_limiter_ref
        self.file_count = 0

    def on_receive(self, msg):
        assert type(msg) == messages.FileDownloadRequestMsg
        self.file_count += 1
        # print(f"Files received: {self.file_count}")
        msg = cast(messages.FileDownloadRequestMsg, msg)
        current_starting_byte = 0
        current_seq_id = 0
        total_chunks = math.ceil(msg.file_size / FileChunkerActor.CHUNK_SIZE_BYTES)
        while current_starting_byte <= msg.file_size:
            last_byte = min(current_starting_byte + FileChunkerActor.CHUNK_SIZE_BYTES - 1, msg.file_size)
            chunk_download_req = messages.ChunkDownloadRequestMsg(
                file_id=msg.file_id,
                s3_bucket=msg.s3_bucket,
                s3_key=msg.s3_key,
                s3_region=msg.s3_region,
                seq_id=current_seq_id,
                total_chunks=total_chunks,
                file_size=msg.file_size,
                first_byte=current_starting_byte,
                last_byte=last_byte
            )

            self.parallel_chunk_downloader_ref.tell(chunk_download_req)
            self.rate_limiter_ref.tell(messages.IncrementWIP())
            current_starting_byte += FileChunkerActor.CHUNK_SIZE_BYTES
            current_seq_id += 1

    def on_stop(self) -> None:
        pass
        # print("FileChunkerActor onstop")

def _work_loop(
        task_queue: mp.Queue,
        result_queue: mp.Queue,
        shutdown_queue: mp.Queue,
        s3_client,
):

    while True:
        try:
            task = task_queue.get(timeout=Config.ACTOR_QUEUE_GET_TIMEOUT)
            assert type(task) == messages.ChunkDownloadRequestMsg
            task = cast(messages.ChunkDownloadRequestMsg, task)

            range_str = f"bytes={task.first_byte}-{task.last_byte}"
            response = s3_client.get_object(Bucket=task.s3_bucket, Key=task.s3_key, Range=range_str)
            content = response["Body"].read()
            result = messages.DownloadedChunkMsg(
                file_id=task.file_id,
                seq_id=task.seq_id,
                total_chunks=task.total_chunks,
                content=content
            )
            result_queue.put(result)
            continue
        except queue.Empty:
            try:
                shutdown_queue.get(block=False)
                return
            except queue.Empty:
                continue
        except KeyboardInterrupt:
            pass
            return
            # print("Keyboard interrupt")
        except Exception as e:
            pass

            # print("Work loop exception", e)


class ParallelChunkDownloader(pykka.ThreadingActor):
    use_daemon_thread = True
    def __init__(self, chunk_sequencer_ref: pykka.ActorRef, rate_limiter_ref: pykka.ActorRef, num_workers=None):
        kwargs = {"chunk_sequencer_ref": chunk_sequencer_ref}
        super().__init__(**kwargs)
        self.chunk_sequencer_ref = chunk_sequencer_ref
        self.rate_limiter_ref = rate_limiter_ref

        if num_workers is None:
            num_workers = mp.cpu_count()

        # Create workers and task queues
        self.task_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.shutdown_queues = [mp.Queue() for _ in range(num_workers)]
        # TODO: Fix client to use correct region.
        self.boto_clients = [boto3.client('s3') for _ in range(num_workers)]  # Instantiating an boto3 client is not multiprocessing safe.
        self.num_workers = num_workers

        self.workers = [
            mp.Process(
                target=_work_loop,
                args=(self.task_queue, self.result_queue, self.shutdown_queues[i], self.boto_clients[i])
            )
            for i in range(num_workers)]

        # Thread that takes worker results and sends them on to the next actor
        self._output_forwarder_stop_signal = threading.Event()
        def _forward_results():
            while not self._output_forwarder_stop_signal.is_set():
                try:
                    result = self.result_queue.get(timeout=Config.ACTOR_QUEUE_GET_TIMEOUT)  # type: messages.DownloadedChunkMsg
                    self.chunk_sequencer_ref.tell(result)
                    self.rate_limiter_ref.tell(messages.DecrementWIP())

                except queue.Empty:
                    pass
        self._output_forwarder = threading.Thread(target=_forward_results)

    def on_start(self) -> None:
        self._output_forwarder.start()
        for worker in self.workers:
            worker.start()

    def on_receive(self, msg):
        assert type(msg) == messages.ChunkDownloadRequestMsg
        msg = cast(messages.ChunkDownloadRequestMsg, msg)
        self.task_queue.put(msg)

    def on_stop(self) -> None:
        self._output_forwarder_stop_signal.set()
        # for worker in self.workers:
        #     worker.terminate()
        for i in range(self.num_workers):
            self.shutdown_queues[i].put(True)
        self._output_forwarder.join()
        # print("ParallelChunkDownloader onstop")

    def on_failure(
        self,
        exception_type: Type[BaseException],
        exception_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        # Do cleanup on failure as well
        self._output_forwarder_stop_signal.set()
        for i in range(self.num_workers):
            self.shutdown_queues[i].put(True)
        self._output_forwarder.join()


class PerFileState:
    def __init__(self, total_chunks_in_file):
        self.total_chunks = total_chunks_in_file
        self.current_seq_id = 0
        self.out_of_order_waiting_room = {}

# TODO: Refactor ChunkSequencer so it can handle multiple files and ends when all files have been downloaded
class ChunkSequencer(pykka.ThreadingActor):
    use_daemon_thread = True
    def __init__(self, output_queue, num_files_tracker_ref: pykka.ActorRef):
        kwargs = {"output_queue": output_queue}
        super().__init__(**kwargs)
        self.output_queue = output_queue
        self.num_files_tracker_ref = num_files_tracker_ref

        self.per_file_state = {}  # type: Dict[str, PerFileState]
        self.num_files_done = 0
        self.total_files = None



    def on_receive(self, msg):
        assert type(msg) == messages.DownloadedChunkMsg
        msg = cast(messages.DownloadedChunkMsg, msg)
        if msg.file_id not in self.per_file_state:
            self.per_file_state[msg.file_id] = PerFileState(msg.total_chunks)

        file_state = self.per_file_state[msg.file_id]
        file_state.out_of_order_waiting_room[msg.seq_id] = msg

        while file_state.current_seq_id in file_state.out_of_order_waiting_room:
            next_result = file_state.out_of_order_waiting_room.pop(file_state.current_seq_id)
            self.output_queue.put(next_result)
            file_state.current_seq_id += 1

        print(f"Sequencer: {msg.file_id}, {file_state.current_seq_id}, {file_state.total_chunks}, {len(list(file_state.out_of_order_waiting_room.keys()))}, {list(file_state.out_of_order_waiting_room.keys())}")

        if file_state.current_seq_id == file_state.total_chunks:
            self.num_files_done += 1
            print(f"All chunks have been sent for file {msg.file_id} ({self.num_files_done} of {self.total_files})")
            if self.total_files is None:
                self.total_files = self.num_files_tracker_ref.ask(messages.QueryNumFiles())
            if self.total_files is not None:
                # TODO: Technically this could complete before the num_tracker gets set, leading to
                #  a hang, but that seems unlikely.
                if self.num_files_done == self.total_files:
                    print("Finished all files")
                    self.output_queue.put(messages.DoneMsg())

    def on_stop(self) -> None:
        pass
        # print("ChunkSequencer onstop")


class RateLimiter(pykka.ThreadingActor):
    use_daemon_thread = True
    def __init__(self):
        super().__init__()
        self.wip = 0

    def on_receive(self, msg):
        assert isinstance(msg, (messages.IncrementWIP, messages.DecrementWIP, messages.QueryWIP))
        if isinstance(msg, messages.IncrementWIP):
            self.wip += 1
        if isinstance(msg, messages.DecrementWIP):
            self.wip -= 1
        if isinstance(msg, messages.QueryWIP):
            return self.wip

    def on_stop(self) -> None:
        pass
        # print("RateLimiter onstop")


class NumFilesTracker(pykka.ThreadingActor):
    use_daemon_thread = True
    def __init__(self):
        super().__init__()
        self.total_num_files = None

    def on_receive(self, msg):
        assert isinstance(msg, (messages.SetNumFiles, messages.QueryNumFiles))
        if isinstance(msg, messages.SetNumFiles):
            self.total_num_files = msg.num_files
        if isinstance(msg, messages.QueryNumFiles):
            return self.total_num_files

    def on_stop(self) -> None:
        pass
        # print("NumFilesTracker onstop")
