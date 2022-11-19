import io
import os
import time
import pstats
import cProfile
from pathlib import Path
from datetime import datetime


def log_profile(log_folder):
    def wrap(func):
        def inner(*args, **kwargs):
            curr_time_hr = datetime.now()
            curr_time_unixs = time.time()

            pr = cProfile.Profile()

            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()

            stream = io.StringIO()
            ps = pstats.Stats(pr, stream=stream).sort_stats('cumulative')
            ps.print_stats()

            report_content = stream.getvalue()

            Path(log_folder).mkdir(parents=True, exist_ok=True)

            log_title = f'{func.__name__} at {curr_time_hr}'
            log_heading = f"{'='*10} {log_title} {'='*10}\n\n"
            log_filename = f"log_{str(curr_time_unixs).replace('.', '_')}.txt"
            log_path = os.path.join(log_folder, log_filename)

            with open(log_path, 'w') as log_f:
                log_f.writelines([log_heading, report_content])

            return retval
        return inner
    return wrap
