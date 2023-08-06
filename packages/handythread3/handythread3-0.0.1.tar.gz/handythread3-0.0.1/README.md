Acknowledgement to original python 2 of handythread in https://github.com/scipy/scipy-cookbook/blob/master/ipython/attachments/Multithreading/handythread.py

simple code snippet

```python3
from handythread import foreach

array_to_update = list(range(10))
def f(x):
    array_to_update[x] += 1
    print (x)
    time.sleep(0.2)
foreach(f,range(10))
    
```
