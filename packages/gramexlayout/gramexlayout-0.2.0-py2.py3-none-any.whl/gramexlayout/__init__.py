'''
This is the module content
'''

import pandas as pd

__all__ = ['subtotal']


def subtotal(data, columns, agg='sum', calc={}, sort_by=None, ascending=True,
             total_label='', total_first=True):
    '''
    Aggregates a DataFrame using one or more columns, with subtotal at every level.

    Parameters:

    - ``data``: DataFrame to aggregate
    - ``columns``: List of columns to group by and calculate subtotals
    - ``agg``: Method of calculating subtotals. Same as `pd.DataFrameGroupBy.aggregate`_.
        - a string, e.g. ``sum``, ``mean``, ``min``, ``median``, ``count``, ``first``, etc.
        - a function, e.g. ``np.sum``
        - a dict of column name -> string/function, for different aggregations by column,
          e.g. ``{'column_a': 'mean', 'column_b': 'sum'}``
    - ``calc``: Used to add new columns. Dict of column name -> function(data) that returns series.
      Same as `DataFrame.assign`_.
      e.g. ``{'price': lambda df: df.sales / df.quantity}``.
    - ``sort_by``: Column name or list of column names to sort by. e.g. ``['Sales', 'Quantity']``
      sorts the first column by ``Sales`` and the second column by ``Quantity``.
    - ``ascending``: Sort ascending or descending. A boolean or list of booleans for each column.
      e.g. ``[True, False]`` sorts the first column ascending and the second column descending.
    - ``total_label``: Label name for the total row. Can be a string, or one string per column.
      e.g. ``['Worldwide', 'Country-wide']`` labels the first column total as ``Worldwide`` and
      the second column total as ``Country-wide``.
    - ``total_first``: Put the total row at the top or bottom. A boolean or list of booleans for
      each column. e.g. ``[True, False]`` puts the first column total at the top and the second
      column total at the bottom.

    .. _pd.DataFrameGroupBy.aggregate: https://bit.ly/3GshLk1
    .. _DataFrame.assign: https://bit.ly/3rRhJOW

    Examples:

    >>> df = pd.DataFrame({
    ...     "Country": ["US", "US", "US", "US", "UK", "UK", "UK", "UK"],
    ...     "City": ["Miami", "Miami", "Omaha", "Omaha", "Leeds", "Leeds", "Derby", "Derby"],
    ...     "Type": ["A", "B", "A", "B", "A", "B", "A", "B"],
    ...     "Sales": [10, 20, 30, 40, 50, 60, 70, 80],
    ...     "Units": [2, 4, 5, 8, 10, 15, 21, 24],
    ... })

    >>> df
      Country   City Type  Sales  Units
    0      US  Miami    A     10      2
    1      US  Miami    B     20      4
    2      US  Omaha    A     30      5
    3      US  Omaha    B     40      8
    4      UK  Leeds    A     50     10
    5      UK  Leeds    B     60     15
    6      UK  Derby    A     70     21
    7      UK  Derby    B     80     24

    Calculate subtotal by Country:

    >>> subtotal(df, 'Country')
             Sales  Units
    Country
               360     89
    US         100     19
    UK         260     70

    Calculate subtotal by Country and City:

    >>> subtotal(df, ['Country', 'City'])
                   Sales  Units
    Country City
                     360     89
    US               100     19
            Miami     30      6
            Omaha     70     13
    UK               260     70
            Leeds    110     25
            Derby    150     45

    Label the totals "Total":

    >>> subtotal(df, ['Country', 'City'], total_label='Total')
                   Sales  Units
    Country City
    Total   Total    360     89
    US      Total    100     19
            Miami     30      6
            Omaha     70     13
    UK      Total    260     70
            Leeds    110     25
            Derby    150     45

    Choose a different total label for each column:

    >>> subtotal(df, ['Country', 'City'], total_label=['World', 'All'])
                   Sales  Units
    Country City
    World   All      360     89
    US      All      100     19
            Miami     30      6
            Omaha     70     13
    UK      All      260     70
            Leeds    110     25
            Derby    150     45

    Move totals to the bottom instead of the top:

    >>> subtotal(df, ['Country', 'City'], total_first=False)
                   Sales  Units
    Country City
    US      Miami     30      6
            Omaha     70     13
                     100     19
    UK      Leeds    110     25
            Derby    150     45
                     260     70
                     360     89

    Move totals to the bottom only for the second column:

    >>> subtotal(df, ['Country', 'City'], total_first=[True, False])
                   Sales  Units
    Country City
                     360     89
    US      Miami     30      6
            Omaha     70     13
                     100     19
    UK      Leeds    110     25
            Derby    150     45
                     260     70

    Aggregate using the mean of values rather than sum:

    >>> subtotal(df, ['Country', 'City'], agg='mean')
                   Sales   Units
    Country City
                    45.0  11.125
    US              25.0   4.750
            Miami   15.0   3.000
            Omaha   35.0   6.500
    UK              65.0  17.500
            Leeds   55.0  12.500
            Derby   75.0  22.500

    Choose a different aggregation for each column:

    >>> subtotal(df, ['Country', 'City'], agg={'Sales': 'mean', 'Units': 'sum'})
                   Sales  Units
    Country City
                      45     89
    US                25     19
            Miami     15      6
            Omaha     35     13
    UK                65     70
            Leeds     55     25
            Derby     75     45

    Add a calculated columns:

    >>> subtotal(df, ['Country', 'City'], calc={'Price': lambda df: df.Sales / df.Units})
                   Sales  Units     Price
    Country City
                     360     89  4.044944
    US               100     19  5.263158
            Miami     30      6  5.000000
            Omaha     70     13  5.384615
    UK               260     70  3.714286
            Leeds    110     25  4.400000
            Derby    150     45  3.333333

    Sort within each level by a column (even a calculated column):

    >>> subtotal(df, ['Country', 'City'], calc={'Price': lambda df: df.Sales / df.Units},
    ...          sort_by='Price')
                   Sales  Units     Price
    Country City
                     360     89  4.044944
    UK               260     70  3.714286
            Derby    150     45  3.333333
            Leeds    110     25  4.400000
    US               100     19  5.263158
            Miami     30      6  5.000000
            Omaha     70     13  5.384615

    Sort Country level by Sales, and City level alphabetically.

    >>> subtotal(df, ['Country', 'City'], sort_by=['Sales', 'City'])
                   Sales  Units
    Country City
                     360     89
    US               100     19
            Miami     30      6
            Omaha     70     13
    UK               260     70
            Derby    150     45
            Leeds    110     25

    Sort Country level by Sales (descending), and City level by Sales (ascending).

    >>> subtotal(df, ['Country', 'City'], sort_by='Sales', ascending=[False, True])
                   Sales  Units
    Country City
                     360     89
    UK               260     70
            Leeds    110     25
            Derby    150     45
    US               100     19
            Miami     30      6
            Omaha     70     13
    '''
    result = []
    columns = columns if isinstance(columns, (list, tuple)) else [columns]

    # Create subtotal for each level -- including grand total (hence the "+1")
    for i in range(len(columns) + 1):
        # Step 1. "Blank" the columns to get the total by setting all values to the total_label.
        # In the first iteration, blank all columns, i.e. set all to '' or 'Total' or whatever.
        # Next iteration, blank all except the first column. And so on.
        blanked = data.assign(**{
            col: _pick(total_label, i + j, '')
            for j, col in enumerate(columns[i:])
        })
        # Step 2. Aggregate and calculate derived columns
        total = blanked.groupby(columns, sort=False).aggregate(agg).assign(**calc)
        # Step 3. Sort by the column for this level. For i=0 (grand total), there's no sorting.
        sort_col = _pick(sort_by, i - 1, None)
        if sort_col is not None:
            total = total.sort_values(sort_col, ascending=_pick(ascending, i - 1, True))
        result.append(total)
    # Step 4. Reindex based on values
    prev = result[1]
    # TODO: This is a bit slow. Optimize
    for i in range(1, len(columns)):
        next, col = result[i + 1], columns[i]
        l2 = _index(prev, prev.reset_index(col).index.values, prev.index.get_level_values(col))
        r2 = _index(next, next.index.droplevel([col]).values, next.index.get_level_values(col))
        out = _concat(l2, r2, total_first, i).reindex(l2.index.get_level_values(0), level=0)
        ix = out.index.get_level_values(0).values
        ix = pd.MultiIndex.from_tuples(ix) if len(columns) > 2 else pd.MultiIndex.from_arrays([ix])
        indices = [ix.get_level_values(i).values for i in range(len(ix.levels))] + [
            out.index.get_level_values(1)]
        prev = _index(out, *indices,
                      names=[c for c in columns if c != col] + [col]).reorder_levels(columns)
    return _concat(result[0], prev, total_first, 0)


def _pick(param, level, default):
    '''
    subtotal() parameters (like sort_by, ascending, etc) can be a single value or a list.
    A single value applies to all group levels. A list applies to each level.

    E.g. sort_by=[a, b] means sort by a for the first level, then sort by b for the second level.
    sort_by=a means sort by a for all levels.

    This function returns the value for a given level.
    If the value is missing for any level, use the default value.
    '''
    if isinstance(param, list):
        return param[level] if 0 <= level < len(param) else default
    return param


def _index(df, *indices, **kwargs):
    return df.set_index(pd.MultiIndex.from_arrays(indices, **kwargs))


def _concat(a, b, total_first, i):
    return pd.concat([a, b]) if _pick(total_first, i, True) else pd.concat([b, a])
