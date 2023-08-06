# AntIPyWidgets

My IPyWidgets

# Installation

```
pip install antipywidgets
```


## Jobs runner

```python 

import antipywidgets.jobs_runner as jobs_runner 

def get_job(...):
    def job():
        ... Do the job ...
    return job

jobs = [get_job(...) for ... in ...]

runner = jobs_runner.make_runner(jobs)
```
![jobs_runner.png](./docs/jobs_runner.png)

In the next cell

```
runner()
```

