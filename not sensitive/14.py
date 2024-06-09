class MemitResult(object):


    def __init__(self, mem_usage, baseline, repeat, timeout, interval,
                 include_children):
        self.mem_usage = mem_usage
        self.baseline = baseline
        self.repeat = repeat
        self.timeout = timeout
        self.interval = interval
        self.include_children = include_children

    def __str__(self):
        max_mem = max(self.mem_usage)
        inc = max_mem - self.baseline
        return 'peak memory: %.02f MiB, increment: %.02f MiB' % (max_mem, inc)

    def _repr_pretty_(self, p, cycle):
        msg = str(self)
        p.text(u'<MemitResult : ' + msg + u'>')


def _get_child_memory(process, meminfo_attr=None, memory_metric=0):

    if isinstance(process, int):
        if process == -1: process = os.getpid()
        process = psutil.Process(process)

    if not meminfo_attr:
        # Use the psutil 2.0 attr if the older version isn't passed in.
        meminfo_attr = 'memory_info' if hasattr(process, 'memory_info') else 'get_memory_info'

    children_attr = 'children' if hasattr(process, 'children') else 'get_children'

    try:
        for child in getattr(process, children_attr)(recursive=True):
            if isinstance(memory_metric, str):
                meminfo = getattr(child, meminfo_attr)()
                yield child.pid, getattr(meminfo, memory_metric) / _TWO_20
            else:
                yield child.pid, getattr(child, meminfo_attr)()[memory_metric] / _TWO_20
    except (psutil.NoSuchProcess, psutil.AccessDenied):

        yield (0, 0.0)
