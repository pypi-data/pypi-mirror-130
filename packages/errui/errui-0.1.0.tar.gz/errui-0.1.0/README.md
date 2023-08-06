# ErrUI

Open a window when an exception is raised and prompt the end user to decide what to do.


## Installation

```sh
python -m pip install errui
```

## Example

### `AbortWindow` (Optional suppression)

This is like `contextlib.suppress` except you get to choose whether to suppress it or to let the exception through and still be raised.

```py
from errui import AbortWindow

with AbortWindow(KeyError):
    {}[0]
```