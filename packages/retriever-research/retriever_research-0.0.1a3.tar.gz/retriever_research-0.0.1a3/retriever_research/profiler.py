from typing import Any

import pykka
import psutil
from datetime import timezone, datetime
import time

from retriever_research.config import Config
from retriever_research.ticker import Ticker


class ProfilerActor(pykka.ThreadingActor):
    def __init__(self):
        self.last_throughput = None
        kwargs = {}
        super().__init__(**kwargs)

    def on_receive(self, message: Any) -> Any:
        timestamp = datetime.now(timezone.utc)
        free_mem_bytes = psutil.virtual_memory().available

        this_process = psutil.Process()
        proc_count = 1
        mem_byte_sum = this_process.memory_info().rss
        for child in this_process.children(recursive=True):
            try:
                proc_count += 1
                mem_byte_sum += child.memory_info().rss
            except psutil.NoSuchProcess:
                pass

        net_io = psutil.net_io_counters()
        cur_time = time.time()
        if self.last_throughput is not None:
            dur = cur_time - self.last_throughput["t"]
            BITS_PER_BYTE = 8
            recv_gbps = (net_io.bytes_recv - self.last_throughput["bytes_recv"] / dur) * BITS_PER_BYTE / Config.GIGA
            sent_gbps = (net_io.bytes_sent - self.last_throughput["bytes_sent"] / dur) * BITS_PER_BYTE / Config.GIGA
        else:
            recv_gbps, sent_gbps = None, None

        self.last_throughput = dict(
            t=cur_time,
            bytes_recv=net_io.bytes_recv,
            bytes_sent=net_io.bytes_sent
        )

        data = dict(used_mb=free_mem_bytes / Config.MEGA, num_procs=proc_count, recv_gbps=recv_gbps, sent_gbps=sent_gbps)
        print(data)


        # print(f"Global mem available: {free_mem_bytes / MEGA }. "
        #       f"Process memory used: {mem_byte_sum / MEGA} "
        #       f"(across {proc_count} processes)")

class ProfilerTick:
    pass


# class ProfilerTicker(Ticker):
#     def execute(self):
#         assert len(self.mem) == 1, "Only 1 actor_ref should be passed to ProfilerTicker.__init__"
#         profiler_actor_ref = self.actor_refs[0]
#         profiler_actor_ref.tell(ProfilerTick())
