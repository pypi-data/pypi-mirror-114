import pytest

from pandas import DataFrame
from pandas.testing import assert_frame_equal
from numpy.testing import assert_array_equal

from tidybear import rename

@pytest.fixture
def df():
    return DataFrame({"A": [1, 2],"B": [3, 4]})

def test_canary():
    pass

def test_rename_no_args(df):
    assert_frame_equal(df, rename(df))
    
def test_rename_with_list(df):
    renamed = rename(df, ["X", "Y"])
    assert renamed.columns.tolist() == ["X", "Y"]
    assert_array_equal(df.values, renamed.values)

def test_rename_with_args(df):
    renamed = rename(df, "X", "Y")
    assert renamed.columns.tolist() == ["X", "Y"]
    assert_array_equal(df.values, renamed.values)
    
def test_rename_all_with_dict(df):
    renamed = rename(df, {"A": "X", "B": "Y"})
    assert renamed.columns.tolist() == ["X", "Y"]
    assert_array_equal(df.values, renamed.values)
    
def test_rename_some_with_dict(df):
    renamed = rename(df, {"B": "Y"})
    assert renamed.columns.tolist() == ["A", "Y"]
    assert_array_equal(df.values, renamed.values)
    
def test_rename_no_cols_dict(df):
    renamed = rename(df, {"C": "Z"})
    assert_frame_equal(df, renamed)
    
def test_rename_all_with_kwargs(df):
    renamed = rename(df, A="X", B="Y")
    assert renamed.columns.tolist() == ["X", "Y"]
    assert_array_equal(df.values, renamed.values)
    
def test_rename_some_with_kwargs(df):
    renamed = rename(df, B="Y")
    assert renamed.columns.tolist() == ["A", "Y"]
    assert_array_equal(df.values, renamed.values)
    
def test_rename_no_cols_kwargs(df):
    renamed = rename(df, C="Z")
    assert_frame_equal(df, renamed)
    
def test_rename_fails_with_list(df):
    # too few
    with pytest.raises(AssertionError):
        rename(df, ["X"])
    
    # too many
    with pytest.raises(AssertionError):
        rename(df, ["X", "Y", "Z"])
        
def test_rename_fails_with_args(df):
    # too few
    with pytest.raises(AssertionError):
        rename(df, "X")
    
    # too many
    with pytest.raises(AssertionError):
        rename(df, "X", "Y", "Z")