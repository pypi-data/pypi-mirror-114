import pandas as pd
from typing import List, Union

from .groupby import GroupBy


class Stat:
    """A way to collect statistics and other summary features within the context of a `GroupBy`.

    The `Stat` class offers 2 ways of defining summary statistics:
    1. Manually creating a `Stat` object and providing the name and series
    2. Using one of the built in summary statistics

    Either way, creating a `Stat` will append it to the active `GroupBy` object, and prior to 
    exiting the with statement, you can call `GroupBy.summarise` to concatenate all your stats into a single dataframe.

    In order to create a `Stat`, you must first have an active GroupBy (using a with statement), otherwise you will get an error.
    
    Examples
    --------
    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>> 
    >>> df = pd.DataFrame({"gr": list("AABB"), "val": [1, 2, 3, 4]})
    >>>
    >>> with tb.GroupBy(df, "gr") as g:
    ...     tb.Stat.size() #auto names "n"
    ...     tb.Stat.mean("val") #auto names "mean_val"
    ...     tb.Stat("first_val", g.val.first())
    ...
    ...     summary = g.summarise()
    ...
    >>> summary
        n  mean_val  first_val
    gr                        
    A   2       1.5          1
    B   2       3.5          3
    ```
    """

    def __init__(self, name: str, series: pd.Series):
        """Create a custom Stat within your GroupBy.

        Parameters
        ----------
        name : str
            What to name the stat
        series : pd.Series
            The values of the stat
        """        
        GroupBy.grouping_is_active()
        GroupBy.active_stats.append(series.rename(name))
    
    @staticmethod
    def size(name="n") -> pd.Series:
        """Compute group sizes.

        Parameters
        ----------
        name : str, optional
            What to name series, by default "n"

        Returns
        -------
        pd.Series
            Number of rows in each group.
        """        
        GroupBy.grouping_is_active()
        Stat(name, GroupBy.active_grouping.size())

    @staticmethod
    def agg(func: Union[str, List[str]], 
            column: str, 
            decimals: int = None, 
            name: str = None, 
            temp:bool = False) -> Union[pd.Series, pd.DataFrame]:
        """Aggregate using one or more operations over the specified variable.

        Parameters
        ----------
        func : str or list
            Function(s) to use for aggregating the data. See pd.Series.agg for acceptable strings.
        column : str
            Name of column to aggregate
        decimals : int, optional
            Number of decimals to round to, by default None
        name : str, optional
            New name of series, by default None. If none the name will be "{func}_{column}". 
            If multiple funcions are provided this parameter is ignored.
        temp : bool, optional, by default False
            If False, the Stat is appended to the active GroupBy. 
            If True, no Stat is appended, and instead the renamed series is returned for further operation.

        Returns
        -------
        Series or DataFrame
        """            
        
        GroupBy.grouping_is_active()
        if isinstance(func, list):
            for f in func:
                Stat.agg(f, column, decimals=decimals)
            return

        if not name:
            name = func + "_" + column

        agg = GroupBy.active_grouping.get(column).agg(func)

        if decimals:
            agg = agg.round(decimals)
        
        if temp:
            return agg
        else:
            Stat(name, agg)

    @staticmethod
    def sum(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute sum of group values.
        
        See `Stat.agg()` for further details.
        """        
        return Stat.agg("sum", column, decimals, name, temp)

    @staticmethod
    def mean(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute mean of group values.
        
        See `Stat.agg()` for further details.
        """     
        return Stat.agg("mean", column, decimals, name, temp)

    @staticmethod
    def median(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute median of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("median", column, decimals, name, temp)

    @staticmethod
    def max(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute max of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("max", column, decimals, name, temp)

    @staticmethod
    def min(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute min of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("min", column, decimals, name, temp)

    @staticmethod
    def var(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute variance of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("var", column, decimals, name, temp)

    @staticmethod
    def std(column: str, decimals: int = None, name: str = None, temp: bool = False):
        """Compute standard deviation of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("std", column, decimals, name, temp)