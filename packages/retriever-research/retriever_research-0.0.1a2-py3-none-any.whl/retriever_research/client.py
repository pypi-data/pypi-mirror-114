import queue
import sys

from retriever_research.actors import ChunkSequencer, ParallelChunkDownloader, FileChunkerActor, FileListGeneratorActor, RateLimiter, NumFilesTracker
from retriever_research.profiler import ProfilerActor
from retriever_research.ticker import ProfilerTicker
from retriever_research.config import Config
from retriever_research import messages



class Retriever:
    def __init__(self):
        self.output_queue = queue.Queue()
        self.active = False

    def start(self):
        self.num_files_tracker = NumFilesTracker.start()
        self.rate_limiter = RateLimiter.start()
        self.chunk_sequencer = ChunkSequencer.start(output_queue=self.output_queue, num_files_tracker_ref=self.num_files_tracker)
        self.parallel_chunk_downloader = ParallelChunkDownloader.start(chunk_sequencer_ref=self.chunk_sequencer, rate_limiter_ref=self.rate_limiter)
        self.file_chunker = FileChunkerActor.start(parallel_chunk_downloader_ref=self.parallel_chunk_downloader, rate_limiter_ref=self.rate_limiter)
        self.file_list_generator = FileListGeneratorActor.start(file_chunker_ref=self.file_chunker, rate_limiter_ref=self.rate_limiter, num_files_tracker_ref=self.num_files_tracker)

        # self.profiler = ProfilerActor.start()
        # self.profiler_ticker = ProfilerTicker(interval=1, actor_refs=self.profiler)
        # self.profiler_ticker.start()

    def shutdown(self):
        self.shutdown_triggered = True
        # Trigger shutdown
        num_files_tracker_stop = self.num_files_tracker.stop(block=False)
        rate_limiter_stop = self.rate_limiter.stop(block=False)
        file_list_generator_stop = self.file_list_generator.stop(block=False)
        file_chunker_stop = self.file_chunker.stop(block=False)
        parallel_chunk_downloader_stop = self.parallel_chunk_downloader.stop(block=False)
        chunk_sequencer_stop = self.chunk_sequencer.stop(block=False)

        # Wait for everything to shutdown
        num_files_tracker_stop.get()
        rate_limiter_stop.get()
        file_list_generator_stop.get()
        file_chunker_stop.get()
        parallel_chunk_downloader_stop.get()
        chunk_sequencer_stop.get()



    def launch(self, s3_bucket, s3_prefix, s3_region):
        self.active = True
        self.file_list_generator.tell(messages.RetrieveRequestMsg(s3_bucket=s3_bucket,
                                                                  s3_prefix=s3_prefix,
                                                                  s3_region=s3_region))
        self.shutdown_triggered = False

    def get_output(self):
        assert self.active, "Cannot call get_output before launching the pipeline"

        while True:
            if self.shutdown_triggered:
                return
            try:
                msg = self.output_queue.get(block=Config.ACTOR_QUEUE_GET_TIMEOUT)
            except queue.Empty:
                continue
            if isinstance(msg, messages.DownloadedChunkMsg):
                pass
                # if msg.seq_id % 10 == 0:
                #     print(f"Received chunk {msg.seq_id+1} of {msg.total_chunks}")
            elif isinstance(msg, messages.DoneMsg):
                print("Received all chunks!")
                break



if __name__ == '__main__':
    ret = Retriever()
    ret.start()
    ret.launch(s3_bucket="quilt-ml", s3_prefix="cv/coco2017/", s3_region="us-east-1")
    # ret.launch(s3_bucket="quilt-ml", s3_prefix="cv/coco2017/annotations/captions_train2017.json", s3_region="us-east-1")
    import time
    # time.sleep(100)
    try:
        ret.get_output()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: shutting down")
        pass
    except Exception as e:
        # print("Exception", e)
        pass
    finally:
        ret.shutdown()
