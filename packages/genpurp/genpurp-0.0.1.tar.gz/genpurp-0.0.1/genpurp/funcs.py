import pandas as pd
import numpy as np
import os
from typing import Any, Callable, List, Optional, Type, Union, Dict

def create_dir(dir_name: Optional[bool] = 'data'):
    """Auxiliar function to create a new directory. User can choose to name
    the specific location.
    Args:
        dir_name (Optional[bool], optional): Directory name. Defaults to 'data'.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def split_groups(data: pd.DataFrame, 
                  columns: Union[str, List[str]], 
                  save: Optional[bool] = False) -> Dict: 
    """Method for grouping data according to a certain(s) column(s) categories.
    User can choose to save or not the grouped data (.csv) to a specific location. 
    The ouput of thismethod is list of pandas DataFrames.

    Args:
        data (pd.DataFrame): Original data.
        columns (Union[str, List[str]]): Target column(s) to group.
        save (Optional[bool], optional): Save to comma-separated values (.csv) files. Defaults to False.

    Returns:
        Dict: Dict of pandas DataFrames.
    """
    dfs = {}
    grp_data = data.groupby(columns)
    for key in grp_data.groups.keys():
        dfs[key] = grp_data.get_group(key)
        if(type(columns) == str):
            out = key
        else:
            out = "_".join(key)
            dfs[out] = dfs.pop(key)
    if(save==True):
        dir_name = ""
        if(type(columns) == str):
            create_dir(columns)
            dfs[out].to_csv(f'{columns}/{out}.csv', index=False)
        else:
            dir_name = "_".join(columns)
            create_dir(dir_name)
            dfs[out].to_csv(f'{dir_name}/{out}.csv', index=False)
    return dfs

def remove_duplicates(df: pd.DataFrame, **kwargs: dict) -> pd.DataFrame:
    """
    Remove duplicates entries
    Args:
        df (pd.DataFrame): DataFrame to check
    Returns:
        pd.DataFrame: DataFrame with duplicates removed
    """
    return df[~(df.duplicated(**kwargs))]


def between(df: pd.DataFrame, column: str, lower, upper) -> pd.DataFrame:
    """
    Remove entreis outside of interval [lower, upper]
    Args:
        df (pd.DataFrame): DataFrame to check
        column (str): column to check
        lower ([type]): interval's lower bound
        upper ([type]): interval's upper bound
    Returns:
        pd.DataFrame: DataFrame with values outside the interval [lower, upper]
        removed
    """
    return df[df[column].between(lower, upper)]


def cvt_to_datetime(df: pd.DataFrame, column: str, **kwargs: dict) -> pd.DataFrame:
    """
    Convert a column to datetime format
    Args:
        df (pd.DataFrame): DataFrame to convert
        column (str): Column to convert to datetime
    Returns:
        pd.DataFrame: DataFrame with column converted to datetime
    """
    df[column] = pd.to_datetime(df[column], **kwargs)
    return df


def cvt_to_ordinal(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Covnert a datetime column to ordinal
    Args:
        df (pd.DataFrame): DataFrame to convert
        column (str): Column to convert to ordinal
    Returns:
        pd.DataFrame: DataFrame with column converted to ordinal
    """
    df[column] = df[column].apply(lambda x: x.toordinal())
    return df


def cvt_to_type(df: pd.DataFrame, column: str, as_type: Type) -> pd.DataFrame:
    """
    Convert a column to the provided dtype
    Args:
        df (pd.DataFrame): DataFrame to convert
        column (str): Column to convert to type
        as_type (Type): Type to convert to
    Returns:
        pd.DataFrame: DataFrame with column converted to type
    """
    df[column] = df[column].astype(as_type)
    return df


def replace(df: pd.DataFrame, column: str, old, new) -> pd.DataFrame:
    """
    Replace a value in the provided column
    Args:
        df (pd.DataFrame): DataFrame to replace
        column (str): Column with values to be replaced
        old ([type]): Value to be replaced
        new ([type]): Value to replace
    Returns:
        pd.DataFrame: DataFrame with column values replaced
    """
    df[column] = df[column].replace(old, new)
    return df


def replace_str(df: pd.DataFrame, column: str, **kwargs) -> pd.DataFrame:
    """
    Replace a substring from the values in a column
    Args:
        df (pd.DataFrame): DataFrame to replace
        column (str): Column with values to be replaced
        kwargs (dict): Extra params to pass to underlying str.replace method
    Returns:
        pd.DataFrame: DataFrame with substring replaced
    """
    df[column] = df[column].str.replace(**kwargs)
    return df


def round_column(df: pd.DataFrame, column: str, decimals: int) -> pd.DataFrame:
    """
    Round a column to the provided number of decimals.
    Note:
        Roounding to 0 decimals does not convert value to integer.
    Args:
        df (pd.DataFrame): DataFrame
        column (str): Column to round
        decimals (int): Number of decimal places to round to
    Returns:
        pd.DataFrame: DataFrame with rounded column
    """
    df[column] = df[column].round(decimals)
    return df


def compare(
    df: pd.DataFrame, left: str, operator: str, right: str = None, value: Any = None
) -> pd.Series:
    """
    Performs a comparisson between two pd.Series or a pd.series and a value.
    Args:
        df (pd.DataFrame): DataFrame to perform comparison
        left (str): Column to perform comparison
        operator (str): operation indicator. Valid operators are eq, ne, lt, le,
        gt, ge, in, ni (not in), and, or.
        right (str, optional): Column to which left will be compared to. Defaults to
        None.
        value (Any, optional): Value to which left will be compared to. If right is
        defined, value is ignored. Defaults to None.
    Raises:
        ValueError: If operator is not valid
    Returns:
        pd.Series[bool]: Result of the comparison
    """
    other = df[right] if right is not None else value
    if operator == "eq":
        return df[left].eq(other)
    elif operator == "ne":
        return df[left].ne(other)
    elif operator == "lt":
        return df[left].lt(other)
    elif operator == "le":
        return df[left].le(other)
    elif operator == "gt":
        return df[left].gt(other)
    elif operator == "ge":
        return df[left].ge(other)
    elif operator == "in":
        try:
            _ = iter(other)
        except TypeError:
            other = [other]
        return df[left].isin(other)
    elif operator == "ni":
        try:
            _ = iter(other)
        except TypeError:
            other = [other]
        return ~df[left].isin(other)
    elif operator == "and":
        return df[left] & other
    elif operator == "or":
        return df[left] | other
    else:
        raise ValueError(
            "Invalid operator. Valid options: eq, ne, lt, le, gt, ge, in, ni (not in), "
            "and, or."
        )


def select_if(
    df: pd.DataFrame,
    left: str,
    operator: str,
    right: str = None,
    value: Any = None,
) -> pd.DataFrame:
    """
    Performs a comparison`left operator right|value` and remove
    entries that do not satisfy it
    Args:
        df (pd.DataFrame): DataFrame to perform selection
        left (str): Column to perform comparison
        operator (str): operation indicator. Valid operators are eq, ne, lt, le,
        gt, ge, in, ni (not in), and, or.
        right (str, optional): Column to which left will be compared to. Defaults to
        None.
        value (Any, optional): Value to which left will be compared to. If right is
        defined, value is ignored. Defaults to None.
    Returns:
        pd.DataFrame: DataFrame with only those entris that satisfy the condition
    """
    return df[compare(df, left, operator, right, value)]


def assign_bool(
    df: pd.DataFrame,
    left: str,
    operator: str,
    right: str = None,
    value: Any = None,
    assign_to: Optional[str] = None,
) -> pd.DataFrame:
    """
    Performs a comparison`left operator right|value` and assign result to
    `assign_to|left` column
    Args:
        df (pd.DataFrame): DataFrame to perform comparison
        left (str): Column to perform comparison
        operator (str): operation indicator. Valid operators are eq, ne, lt, le,
        gt, ge, in, ni (not in), and, or.
        right (str, optional): Column to which left will be compared to. Defaults to
        None.
        value (Any, optional): Value to which left will be compared to. If right is
        defined, value is ignored. Defaults to None.
        assign_to (Optional[str], optional): Column to store the result of the
        condition.
        If None, result is assigned to the `left` column. Defaults to None.
    Returns:
        pd.DataFrame: DataFrame with `left|assign_to` column storing the result
        of the comparison
    """
    _assign_to = left if assign_to is None else assign_to
    df[_assign_to] = compare(
        df=df, left=left, operator=operator, right=right, value=value
    )
    return df


def replace_if(
    df: pd.DataFrame, column: str, operator: str, mask_value: Any, replace_value: Any
) -> pd.DataFrame:
    """
    Replace values that satisfy the condition `column operator mask_value` with
    `replace_value`
    Args:
        df (pd.DataFrame): DataFrame to perform selection
        left (str): Column to perform comparison
        operator (str): operation indicator. Valid operators are eq, ne, lt, le,
        gt, ge, in, ni (not in), and, or.
        mask_value (Any): Comparison value
        replace_value (Any): Replacement value
    Returns:
        pd.DataFrame: DataFrame with values replaced
    """
    _mask = compare(df=df, left=column, operator=operator, value=mask_value)
    df[column] = df[column].mask(_mask, replace_value)
    return df


def busday_count(
    df: pd.DataFrame, column: str, col_begin: str, col_end: str
) -> pd.DataFrame:
    """
    Count the number of busy days between the provided datetime interval
    [col_begin, col_end] and assign the result to `column`
    Args:
        df (pd.DataFrame): DataFrame
        column (str): Column to assign result to
        col_begin (str): Column with the initial dates
        col_end (str): Column with the final dates
    Returns:
        pd.DataFrame: DataFrame with `column` storing the number of
        busy days in the interval [col_begin, col_end]
    """
    df[column] = np.busday_count(
        pd.to_datetime(df[col_begin]).values.astype("datetime64[D]"),
        pd.to_datetime(df[col_end]).values.astype("datetime64[D]"),
    )
    return df


def math_operation(
    df: pd.DataFrame,
    left: str,
    operator: str,
    right: str = None,
    value: Any = None,
    assign_to: Optional[str] = None,
) -> pd.DataFrame:
    """
    Performs a mathematical operation between two pd.Series or a pd.Series and a value.
    Args:
        df (pd.DataFrame): DataFrame to perform operation
        left (str): Column to perform operation (left side)
        operator (str): operation indicator. Valid operators are +, -, /, *.
        right (str, optional): Column to perform operation (right side). Defaults to
        None.
        value (Any, optional): Value to perform operation (right side). If right is
        defined, value is ignored. Defaults to None.
        assign_to (Optional[str], optional): Column to store the result of the
        operation. If None, result is assigned to the `left` column. Defaults to None.
    Returns:
        pd.DataFrame: DataFrame with `left|assign_to` column storing the result
        of the operation
    """

    _assign_to = assign_to or left
    df[_assign_to] = df[left].copy()
    other = df[right] if right is not None else value

    if operator == "+":
        df[_assign_to] = df[left] + other
    elif operator == "-":
        df[_assign_to] = df[left] - other
    elif operator == "/":
        df[_assign_to] = df[left] / other
    elif operator == "*":
        df[_assign_to] = df[left] * other

    return df


def select_columns(
    df: pd.DataFrame, columns: Union[str, List[str]]
) -> Union[pd.DataFrame, pd.Series]:
    """
    Select columns from a DataFrame
    Args:
        df (pd.DataFrame): DataFrame
        columns (Union[str, List[str]]): column(s) to select
    Returns:
        Union[pd.DataFrame, pd.Series]: Series or DataFrame with
        selected columns
    """
    if isinstance(columns, str):
        columns = [columns]

    return df.loc[:, columns]


def concat_str(
    df: pd.DataFrame,
    columns: List[str],
    assign_to: Optional[str] = None,
    drop: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Concatenate the values of `columns` and assign to `assign_to|columns[0]`.
    Args:
        df (pd.DataFrame): DataFrame
        columns (List[str]): Columns to concatenate
        assign_to (Optional[str], optional): Column to assign result to
        If None assign to the first column from `columns`. Defaults to None.
        drop (bool): Whether to drop the columns used for concatenation. If assign_to
        is None, drop all `columns` but the first, else drop all `columns`. Defaults to
        False.
    Returns:
        pd.DataFrame: DataFrame with `columns` concatenated
    """
    _assign_to = assign_to or columns[0]
    df[_assign_to] = df.loc[:, columns].astype(str).apply("".join, axis=1, raw=True)
    if drop:
        df.drop(
            columns=(columns if assign_to is not None else columns[1:]),
            inplace=True,
        )
    return df


def combine_columns(
    df: pd.DataFrame,
    column: str,
    other: str,
    comb_func: Callable,
    assign_to: Optional[str] = None,
) -> pd.DataFrame:
    """
    Combine the Series with a Series according to comb_func.
    Args:
        df (pd.DataFrame): [description]
        column (str): Column to combine
        other (str): Column to be combined
        comb_func (Callable): Function that takes two scalars as inputs and returns an
        element
        assign_to (Optional[str], optional): Column to assign result to. If None,
        assign result to `column`. Defaults to None.
    Returns:
        pd.DataFrame: [description]
    """
    _assign_to = assign_to or column
    df[_assign_to] = df[column].combine(other=df[other], func=comb_func)
    return df


def df_map(
    df: pd.DataFrame, column: str, assign_to: Optional[str] = None, *args, **kwargs
) -> pd.DataFrame:
    """
    Wrapper for pd.Series.map() to use on pd.DataFrame.pipe().
    Args:
        df (pd.DataFrame): DataFrame
        column (str): Column to call map method
        assign_to (str, optional): Column to assign result to. If None, assign result
        to `column`. Defaults to None.
    Returns:
        pd.DataFrame: DataFrame with map method called on `column` and result assigned
        to `assign_to|column` column.
    """
    _assign_to = assign_to or column
    df[_assign_to] = df[column].map(*args, **kwargs)
    return df