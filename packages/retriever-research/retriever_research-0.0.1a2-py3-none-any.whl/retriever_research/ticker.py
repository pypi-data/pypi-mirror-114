import queue
import threading

import pykka
from typing import List, Union
import time


class Ticker(threading.Thread):
    def __init__(self, interval=10, actor_refs: Union[None, List[pykka.ActorRef], pykka.ActorRef] = None) -> None:
        self.shutdown_queue = queue.Queue()
        self.interval = interval

        self.actor_refs = actor_refs if actor_refs is not None else []
        if not isinstance(self.actor_refs, List):
            self.actor_refs = [self.actor_refs]
        super().__init__()

    def stop(self):
        self.shutdown_queue.put(None)

    def execute(self):
        print(time.time())

    def run(self):
        self.next_scheduled_time = time.time()
        while True:
            try:
                wait_time = max(0.0, self.next_scheduled_time - time.time())
                msg = self.shutdown_queue.get(block=True, timeout=wait_time)
                # Receive a shutdown message
                return
            except queue.Empty:
                self.next_scheduled_time = time.time() + self.interval
                self.execute()


class ProfilerTick:
    pass


class ProfilerTicker(Ticker):
    def execute(self):
        assert len(self.actor_refs) == 1, "Only 1 actor_ref should be passed to ProfilerTicker.__init__"
        profiler_actor_ref = self.actor_refs[0]
        profiler_actor_ref.tell(ProfilerTick())
