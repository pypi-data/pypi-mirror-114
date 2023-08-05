import ipysheet
import ipywidgets as widgets
import traceback
from typing import Dict, Callable
from IPython.display import display


def make_runner(jobs: Dict[str, Callable]) -> Callable:
    """
    Display initial run board

    Parameters
    ----------
    jobs: Dict[str,Callable]
        Jobs to run

    Returns
    -------
    Callable
        Should be called to run jobs
    """

    jobs_count = len(jobs)

    sheet = ipysheet.sheet(columns=3, rows=jobs_count, column_headers=["Name", "Status", "Message"])
    ipysheet.column(0, [name for name in jobs.keys()], read_only=True)
    ipysheet.column(1, ["Pending...." for _ in jobs.keys()], read_only=True)
    ipysheet.column(2, ["" for _ in jobs.keys()], read_only=True)

    display(sheet)
    
    def run_func():
        for idx, (job_name, job_func) in enumerate(jobs.items()):
            print(f"Run '{job_name}'")
            try:
                _ = job_func()
                ipysheet.cell(idx, 1, widgets.Valid(value=True, description="Passed"))
            except Exception as e:
                err = traceback.format_exc()
                ipysheet.cell(idx, 1, widgets.Valid(value=False, description="Failed"))
                ipysheet.cell(idx, 2, widgets.Textarea(err))
    
    return run_func