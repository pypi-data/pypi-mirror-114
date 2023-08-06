import pykka
import queue

from retriever_research.actors import ChunkSequencer, ParallelChunkDownloader, FileChunker, FileListGenerator
from retriever_research.observability import LoggingActor, ObservabilityTicker
from retriever_research.config import Config
from retriever_research import messages
from retriever_research.shared_memory import SharedMemory


class Retriever:
    def __init__(self):
        self.active = False
        self.shutdown_triggered = False
        self.output_queue = queue.Queue()

        # Create the log actor first so we can log
        self.log_actor_ref = LoggingActor.start(output_file="retriever.log")
        self.mem = SharedMemory(log_actor_ref=self.log_actor_ref)
        # self.mem.register_actor(Config.OBSERVABILITY_URN, self.observability_actor_ref)

        # Start all the other actors in multiple steps. Create actor, register into our custom registry,
        # then start the actor loop.
        # NOTE: __init__() executes during create().
        # NOTE: on_start() executes at the beginning of the actor loop.
        file_list_generator = FileListGenerator.create(mem=self.mem)
        file_chunker = FileChunker.create(mem=self.mem)
        parallel_chunk_downloader = ParallelChunkDownloader.create(mem=self.mem)
        chunk_sequencer = ChunkSequencer.create(mem=self.mem, output_queue=self.output_queue)

        file_list_generator.start_actor_loop()
        file_chunker.start_actor_loop()
        parallel_chunk_downloader.start_actor_loop()
        chunk_sequencer.start_actor_loop()

        # Actor-like threads that don't fit into the Pykka model.
        self.obs_ticker = ObservabilityTicker(mem=self.mem, interval=1)

    def shutdown(self):
        self.shutdown_triggered = True

        # The observability ticker need to be shut down first because it watches the other actors
        self.obs_ticker.stop()
        self.obs_ticker.join()

        # Trigger shutdown
        stops = []
        stops.append(pykka.ActorRegistry.get_by_urn(Config.FILE_LIST_GENERATOR_URN).stop(block=False))
        stops.append(pykka.ActorRegistry.get_by_urn(Config.FILE_CHUNKER_URN).stop(block=False))
        stops.append(pykka.ActorRegistry.get_by_urn(Config.PARALLEL_CHUNK_DOWNLOADER_URN).stop(block=False))
        stops.append(pykka.ActorRegistry.get_by_urn(Config.CHUNK_SEQUENCER_URN).stop(block=False))

        # Wait for everything to shutdown.
        [s.get() for s in stops]

        # Observability goes at the end so logging is available during shutdown
        pykka.ActorRegistry.get_by_urn(Config.OBSERVABILITY_URN).stop(block=True)

    def launch(self, s3_bucket, s3_prefix, s3_region):
        self.active = True
        launch_msg = messages.RetrieveRequestMsg(s3_bucket=s3_bucket,
                                                 s3_prefix=s3_prefix,
                                                 s3_region=s3_region)
        pykka.ActorRegistry.get_by_urn(Config.FILE_LIST_GENERATOR_URN).tell(launch_msg)
        self.obs_ticker.start()

    # TODO: Rewrite this
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
