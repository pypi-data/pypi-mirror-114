import pandas as pd

from typing import Union, List


def count(df: pd.DataFrame, 
          columns: Union[List[str], str], 
          sort: bool = False, 
          name: str = None) -> pd.DataFrame:
    """Quickly count the unique values of one or more variables.

    Parameters
    ----------
    df : DataFrame
        The dataframe to use
    columns : str or list
        The column(s) to group by.
    sort : bool, optional
        If True, will show the largest groups at the top., by default False
    name: str, optional
        What to rename the new column with counts. By default "n" is used.
    """

    name = name if name else "n"
    counts = df.groupby(columns).size().rename(name).reset_index()
    if sort:
        return counts.sort_values(name, ascending=False)
    else:
        return counts.sort_values(columns)


def top_n(df: pd.DataFrame, order_by: str, n: int, negate: bool = False, groupby: str = None):
    """Get the top N elements of a dataframe of group.

    Parameters
    ----------
    df : DataFrame
    order_by : str
        The column to order the values by
    n : int
        The number of elements to get
    negate: bool, optional
        Sort the values from smallest to largest and get the n smallest values.,
        by default False
    groupby : str or list, optional
        Get top n elements by group. These columns used for groupby, by default None

    Returns
    -------
    Dataframe
    """    
    df = df.copy()
    if groupby:
        return df.groupby(groupby) \
            .apply(lambda x: top_n(x, order_by, n, negate)) \
            .reset_index(drop=True)

    return df.sort_values(order_by, ascending=negate).head(n)


def rename(df: pd.DataFrame, *args, **kwargs):
    """Rename the columns of a dataframe
    
    You can use this function is a few different ways. 
    - Use a list of strings to be used as the new column names. 
    In this case the length of the list must equal the number of columns in the dataframe.
    - Use the new column names as arguments to the function. Again the number of arguments passed
    must equal the number of columns in the dataframe. 
    - Use a dictionary with the keys as existing column names and values as the new column names.
    - Use keyword arguments with the key as existing column names and values as the new columns names.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    DataFrame
    
    Examples
    --------
    
    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>>
    >>> df = pd.DataFrame({"A": [1, 2],"B": [3, 4]})
    >>> df
    A  B
    0  1  3
    1  2  4
    >>> tb.rename(df, ["X", "Y"])
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, "X", "Y")
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, {"A": "X", "B": "Y"})
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, A="X", B="Y")
    X  Y
    0  1  3
    1  2  4
    ```
    """    
    df = df.copy()
    if len(kwargs) > 0:
        return df.rename(columns=kwargs)
    
    if len(args) == 1 and isinstance(args[0], dict):
        return df.rename(columns=args[0])
    
    if len(args) >= 1:
        new_cols = args[0] if isinstance(args[0], list) else list(args)
        
        assert len(new_cols) == df.shape[1], \
            f"Number of columns provided ({len(new_cols)}) " \
            f"does not match the number of features in the dataframe ({df.shape[1]})."
        
        df.columns = new_cols
        return df
    
    return df