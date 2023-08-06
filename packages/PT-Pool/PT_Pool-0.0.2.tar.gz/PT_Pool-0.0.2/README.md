
## What PT\_Pool?

It's a combined process+threading pool. (having only "apply\_async" method for now)  

ThreadPoolExecutor on its own doesn't utilize more than one CPU core.  
ProcessPoolExecutor on its own is not suitable to provide concurrency (e.g. slows down the system when large number of processes are created, and doesn't allow to create more than around 1000 processes on my system).  

## Installation

`python3.7 -m pip install PT_Pool`  


## Usage

```python
from PT_Pool import PT_Pool
import time

def f(x):
    time.sleep(1)
    return x*x

def on_result(res):
    print(res)

pt_pool = PT_Pool(threads_limit = 100)

pt_pool.apply_async(f, range(10), on_result=on_result)

time.sleep(2)
input('Press enter to exit...')
```

    

