import multiprocessing
import time
from .termination import terminate_process

# Also see https://blog.pelicandd.com/article/191


def read_file(file, exit_event, action):
    can_terminate = multiprocessing.Event()
    args = (file, exit_event, action, can_terminate)
    _run_terminable_process(_read_file_internal, args, can_terminate)


def read_file_into_queue(file, exit_event, queue, transform=None):
    """
    Processes the lines from a file in a loop, putting them in a queue as they
    arrive. The method can be used to read from `stdin`, or from an arbitrary
    file.
    """
    def action(line):
        processed = transform(line) if transform else line
        queue.put(processed)

    read_file(file, exit_event, action)


def _run_terminable_process(target, args, can_terminate):
    subprocess_name = multiprocessing.current_process().name + "^"
    p = multiprocessing.Process(name=subprocess_name, target=target, args=args)
    p.start()

    while not exit_event.is_set():
        time.sleep(0.01)

    if can_terminate.is_set():
        # The process is just waiting for data in a stream, and therefore can
        # be safely terminated.
        p.terminate()
    else:
        terminate_process(p)


def _read_file_internal(file, exit_event, action, can_terminate):
    with open(file) as f:
        while not exit_event.is_set():
            can_terminate.set()
            line = f.readline().strip()

            can_terminate.clear()
            if line and not exit_event.is_set():
                action(line)

