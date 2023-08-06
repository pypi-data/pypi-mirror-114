# TidyBear

A tidier approach to pandas.

___

## Examples

```python
import numpy as np
import pandas as pd

import tidybear as tb

df = pd.DataFrame({
    "gr": list("AAABBBB"),
    "x": [1, 2, 3, 7, 8, 8, 9],
    "y": [4, 5, 6, 1, 1, 1, 1],
    "z": [2, 4, 6, 0, 1, 2, 2]
})
```

## Functions

```python
# Count by group
tb.count(df, "gr")

# Top n rows ordered by some row
tb.top_n(df, order_by="x", n=3)

# rename columns more quickly
tb.rename(df, x="a")
```

## Groupby and Summarise

```python
with tb.GroupBy(df, "gr") as g:
    
    # built in statistcs
    g.n()
    g.sum("x")
    
    # multiple aggs to a single column
    g.agg("x", ["mean", "median"])
    
    # same agg across multiple columns using built in
    g.mean(["y", "z"])
    
    # multiple aggs across multiple columns
    g.agg(["y", "z"], ["median", "std"])
    
    # send a lambda function to agg
    g.agg("x", lambda x: len(x.unique()), name="n_distinct_x1")
    
    # Use 'temp' keyword to return series and use it later
    max_val = g.max("x", temp=True)
    min_val = g.min("x", temp=True)
    
    # create a custom stat directly
    g.stat("midpoint", (max_val + min_val) / 2)
    
    summary = g.summarise() # or g.summarize()
```