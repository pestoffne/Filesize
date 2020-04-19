# Filesize

# Example

```python
In [1]: from filesize import Filesize as f

In [2]: f('23MiB') * 0.02
Out[2]: 471.04KiB
    
In [3]: f(1024, 'KB')
Out[3]: 1000.0KiB

In [4]: f('200MB') + f('0.5GiB') + 2 * f('55MiB')
Out[4]: 812.73MiB
```
