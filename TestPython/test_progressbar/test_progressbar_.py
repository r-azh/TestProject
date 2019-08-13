#     Original source: https://stackoverflow.com/a/15860757/1391441
import sys
import time
from datetime import datetime


class ProgressBar:
    total = None
    run_count = None
    _progressed = 0

    def __init__(self, total, bar_length=20):
        self.total = total
        self.run_count = 0
        self.bar_length = bar_length

    def next(self, progress=1, eta=None):
        status = ""
        self._progressed = self._progressed + progress
        progress = float(self._progressed) / float(self.total)
        if progress >= 1.:
            progress, status = 1, "\r\n"
        block = int(round(self.bar_length * progress))
        text = "\r[{}] {:.0f}% {}".format(
            "#" * block + "-" * (self.bar_length - block), round(progress * 100, 0),
            status)
        if eta is not None:
            text += f" ETA:{eta}"
        sys.stdout.write(text)
        sys.stdout.flush()


def compute_eta(last_mean_time, iteration, current_duration, total_iterations):
    if iteration == 0:
        return current_duration, (current_duration * (total_iterations - 1))

    mean_time = ((last_mean_time * (iteration - 1)) + current_duration) / iteration
    return mean_time, (mean_time * (total_iterations - iteration))


runs = 300
progressbar = ProgressBar(runs)
mean_time = 0
for run_num in range(runs):
    start_time = datetime.utcnow()

    time.sleep(.01)

    duration = datetime.utcnow() - start_time
    mean_time, eta = compute_eta(mean_time, run_num, duration, runs)

    if run_num == runs - 1:
        eta = None

    progressbar.next(eta=eta)