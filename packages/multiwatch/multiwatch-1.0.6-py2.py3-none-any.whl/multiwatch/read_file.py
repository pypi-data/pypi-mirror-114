import multiprocessing
import time
from .termination import terminate_process


def read_file(file, exit_event, action):
    can_terminate = multiprocessing.Event()
    process_name = multiprocessing.current_process().name
    p = multiprocessing.Process(
        name=process_name + "^",
        target=_read_file_internal,
        args=(file, exit_event, action, can_terminate)
    )
    p.start()

    while not exit_event.is_set():
        time.sleep(0.01)

    if can_terminate.is_set():
        # The process is just waiting for data in a stream, and therefore can
        # be safely terminated.
        p.terminate()
    else:
        terminate_process(p)


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


def _read_file_internal(file, exit_event, action, can_terminate):
    with open(file) as f:
        line = None
        while not exit_event.is_set():
            if line:
                action(line)

            can_terminate.set()
            line = f.readline().strip()
            can_terminate.clear()
