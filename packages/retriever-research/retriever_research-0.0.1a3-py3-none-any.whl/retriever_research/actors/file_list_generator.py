import boto3
import time
from typing import Type
from types import TracebackType
import pykka

from retriever_research import messages
from retriever_research.config import Config
from retriever_research.shared_memory import SharedMemory
from retriever_research.actors.pykka_extensions.custom_actor import RetrieverThreadingActor

class FileListGenerator(RetrieverThreadingActor):
    use_daemon_thread = True

    def __init__(self, mem: SharedMemory):
        super().__init__(urn=Config.FILE_LIST_GENERATOR_URN)
        self.mem = mem

        # Can't set ref in init as other actors may not have been created yet
        self.file_chunker_ref = None

    def on_start(self) -> None:
        self.file_chunker_ref = pykka.ActorRegistry.get_by_urn(Config.FILE_CHUNKER_URN)

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
                while self.mem.get_wip() > Config.MAX_WIP:
                    time.sleep(Config.TOO_MUCH_WIP_SLEEP_TIME)


                file_id = f"s3://{msg.s3_bucket}/{key}"
                self.file_chunker_ref.tell(messages.FileDownloadRequestMsg(
                    file_id=file_id,
                    s3_bucket=msg.s3_bucket,
                    s3_key=key,
                    s3_region=msg.s3_region,
                    file_size=size
                ))
                num_files += 1
                self.log(f"Requested download of {file_id} (#{num_files})")

        self.log(f"Setting total file count to {num_files}")
        self.mem.set_total_file_count(num_files)

        if num_files == 0:
            raise RuntimeError("No files match prefix")

    # def on_stop(self) -> None:
    #     print("FileListGeneratorActor onstop")

    # def on_failure(
    #     self,
    #     exception_type: Type[BaseException],
    #     exception_value: BaseException,
    #     traceback: TracebackType,
    # ) -> None:
    #     print(f"FileListGeneratorActor on failure, {exception_type}, {exception_value}")
