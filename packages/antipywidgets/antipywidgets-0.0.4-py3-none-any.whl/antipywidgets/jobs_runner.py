import ipywidgets as widgets
from ipywidgets import Button, GridBox, Layout, ButtonStyle, VBox, HBox, Label, Valid, Textarea
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


    def make_new_row(name):
        name = Label(value=name, layout=Layout(width='10%'))

        status = VBox([Label(value="Pending...")], layout= Layout(width='10%')) #Valid(value=status, )

        message = Textarea(value="", disabled=True, layout=Layout(width='80%'))

        return [name,status,message]
    
    jobs_and_rows = [{"job_name": job_name, "job_func":job_func, "row": make_new_row(job_name)} for job_name, job_func in jobs.items() ]

    table = VBox([HBox(i["row"]) for i in jobs_and_rows] )

    display(table)
    
    def run_func():
        for job in jobs_and_rows:
            job_name = job["job_name"]
            job_func = job["job_func"]
            row = job["row"]
            print(f"Run '{job_name}'")
            status = row[1]
            message = row[2]
            try:
                _ = job_func()
                
                status.children = [Valid(value=True, description="Passed")]
            except Exception as e:
                err = traceback.format_exc()
                status.children = [Valid(value=False, description="Failed")]
                message.value = err
    return run_func