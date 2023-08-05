# nbhistory
> Enable saving current notebook execution history as a notebook


## Install

`pip install nbhistory`

## How to use

```
from nbhistory.core import save_notebook_history

save_notebook_history('tmp/my_history.ipynb')
```

    Notebook history saved to tmp/my_history.ipynb


## Limitation

nbhistory only saves the execution history, markdown cells will not be saved.
