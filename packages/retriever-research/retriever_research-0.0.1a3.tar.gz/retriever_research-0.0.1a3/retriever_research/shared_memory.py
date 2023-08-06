# Threadsafe shared memory. Use this rarely - communication is typically better.
# The pykka actor registry won't let you set the URN by hand, instead always
# generating a uuid4. We add our own custom registry here to allow reference
# by predefined URN
import datetime
import threading

import pykka
from retriever_research import messages
from retriever_research.config import Config, LogLevels

class RetrieverRegistryError(Exception):
    pass

class SharedMemory:
    def __init__(self, log_actor_ref: pykka.ActorRef):
        self._wip_lock = threading.Lock()
        self._wip = 0

        self._total_file_count_lock = threading.Lock()
        self._total_file_count = None

        self.log_actor_ref = log_actor_ref
        self.logging = Logger(log_actor_ref=self.log_actor_ref)

    def increment_wip(self):
        with self._wip_lock:
            self._wip += 1

    def decrement_wip(self):
        with self._wip_lock:
            self._wip -= 1

    # TODO: Does this actually need to use a lock? The exact value isn't super important
    def get_wip(self):
        with self._wip_lock:
            return self._wip

    def set_total_file_count(self, total_file_count: int):
        with self._total_file_count_lock:
            self._total_file_count = total_file_count

    def get_total_file_count(self):
        with self._total_file_count_lock:
            return self._total_file_count


class Logger:
    def __init__(self, log_actor_ref: pykka.ActorRef):
        self.log_actor_ref = log_actor_ref

    def log(self, actor_urn: str, detail: str, level: LogLevels):
        log_msg = messages.LogMessage(
            actor=actor_urn,
            log=detail,
            level=level,
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.log_actor_ref.tell(log_msg)


