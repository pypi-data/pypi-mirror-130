from __future__ import annotations

from lumipy.common.string_utils import indent_str
from ..base_sql_expression import BaseSqlExpression
from ..column.column_base import BaseColumnExpression
from ..column.column_ordering import BaseColumnOrdering
from ..sql_value_type import SqlValType
from .partition import WindowPartition
from .order import WindowOrder
from .frame import WindowFrame
from typing import Iterable, Optional, Union, Any
from .function import (
    FirstValue, LastValue, Lag, Lead,
    NthValue, WindowMean, WindowCount, WindowMax, WindowMin,
    WindowSum, CumeDist, DenseRank, Rank, NTile,
    RowNumber, PercentRank
)
from lumipy.query.expression.column.column_literal import python_to_expression


class Over(BaseSqlExpression):
    """Class representing the OVER clause in a SQL window function specification.

    """

    def __init__(
            self,
            partitions: Optional[WindowPartition],
            orders: Optional[WindowOrder],
            frame: Optional[WindowFrame],
    ):
        """Constructor for the Over class. User must provide at least one of a window partition object, a window order
        object or a window frame object.

        Args:
            partitions (Optional[WindowPartition]): optional window partition object.
            orders (Optional[WindowPartition]): optional window ordering object.
            frame (Optional[WindowPartition]): optional window frame objecy.
        """

        if all(x is None for x in [partitions, orders, frame]):
            raise ValueError(
                'Over objects must be created with one or more of WindowPartition, WindowOrder, '
                'or WindowFrame objects.'
            )

        self.frame = frame
        # Handle the case where these are unspecified and equal to None
        # None is replaced by a null literal node and can be used in recomposing the DAG after decomposing it
        # Expression types just pass through this function unaffected.
        self.partitions = python_to_expression(partitions)
        self.orders = python_to_expression(orders)

        if self.partitions.get_type() != SqlValType.Null and not isinstance(partitions, WindowPartition):
            raise TypeError(f"partitions arg must be a WindowPartition instance or None. Was {type(partitions).__name__}")
        if self.orders.get_type() != SqlValType.Null and not isinstance(orders, WindowOrder):
            raise TypeError(f"orders arg must be a WindowOrder instance or None. Was {type(orders).__name__}")
        if not isinstance(frame, WindowFrame):
            raise TypeError(f"frame arg must be a WindowFrame instance. Was {type(frame).__name__}")

        def sql_str_fn(*args):
            content = [a.get_sql() for a in args if a.get_type() != SqlValType.Null]
            content_str = '\n'.join(content) + '\n)'
            return f"OVER(\n{indent_str(content_str, n=4)}"

        super().__init__(
            'window',
            sql_str_fn,
            lambda *args: True,
            lambda *args: SqlValType.Window,
            self.partitions,
            self.orders,
            self.frame
        )

    def first(self, expression: BaseColumnExpression) -> FirstValue:
        """Get the value of an expression for the first row in the window.

        Args:
            expression (BaseColumnExpression): column expression to evaluate at the first row.

        Returns:
            FirstValue: first window function instance representing this expression.
        """
        return FirstValue(self, expression)

    def last(self, expression: BaseColumnExpression) -> LastValue:
        """Get the value of an expression for the last row in the window.

        Args:
            expression (BaseColumnExpression): column expression to evaluate at the last row.

        Returns:
            LastValue: last window function instance representing this expression.
        """
        return LastValue(self, expression)

    def lag(self, expression: BaseColumnExpression, offset: Optional[int] = 1, default: Optional[Any] = None) -> Lag:
        """Apply a lag window expression: get the value of an expression n places behind the current row in the window.

        For example for n = 1 evaluated at row 3 it will yield the value at row 2. If the lag row is out of the window
        range a default value will be returned.

        Args:
            expression (BaseColumnExpression): the column expression to evaluate with lag.
            offset (Optional[int]): the number of places behind to evaluate at (defaults to 1)
            default (Optional[Any]): the default value to assign to out of range lag rows (defaults to None, which is
            considred to be equal to NULL in SQL)

        Returns:
            Lag: lag window function expression instance.
        """
        return Lag(self, expression, offset, default)

    def lead(self, expression: BaseColumnExpression, offset: Optional[int] = 1, default: Optional[Union[Any]] = None) -> Lead:
        """Apply a lead window expression: get the value of an expression n places in front the current row in the window.

        For example for n = 1 evaluated at row 2 it will yield the value at row 3. If the lead row is out of the window
        range a default value will be returned.

        Args:
            expression (BaseColumnExpression): the column expression to evaluate with lead.
            offset (Optional[int]): the number of places behind to evaluate at (defaults to 1)
            default (Optional[Any]): the default value to assign to out of range lead rows (defaults to None, which is
            considred to be equal to NULL in SQL)

        Returns:
            Lead: lead window function expression instance.
        """
        return Lead(self, expression, offset, default)

    def nth_value(self, expression: BaseColumnExpression, n: int) -> NthValue:
        """Apply an nth value expression: get the value of the expression at position n in the window.

        Args:
            expression (BaseColumnExpression): the expression to evaluate at the nth row
            n (int): the value of n to use.

        Returns:
            NthValue: nth value window function expression instance.
        """
        return NthValue(self, expression, n)

    def mean(self, expression: BaseColumnExpression) -> WindowMean:
        """Apply a mean (AVG) aggregation expression: get the mean value of the expression in a window.

        Args:
            expression (BaseColumnExpression): expression to take the mean of in the window.

        Returns:
            WindowMean: mean value window function expression instance.
        """
        return WindowMean(self, expression)

    def count(self, expression: BaseColumnExpression) -> WindowCount:
        """Apply a count aggregation expression: count the number of rows where the expression is not null.
        todo: check nulls aren't counted.

        Args:
            expression (BaseColumnExpression): expression to evaluate in the count.

        Returns:
            WindowCount: count window function.
        """
        return WindowCount(self, expression)

    def max(self, expression: BaseColumnExpression) -> WindowMax:
        """Apply a max aggregation expression: get the max value of the expression in a window.

        Args:
            expression (BaseColumnExpression): expression to take the max of in the window.

        Returns:
            WindowMax: max value window function expression instance.
        """
        return WindowMax(self, expression)

    def min(self, expression: BaseColumnExpression) -> WindowMin:
        """Apply a min aggregation expression: get the min value of the expression in a window.

        Args:
            expression (BaseColumnExpression): expression to take the min of in the window.

        Returns:
            WindowMin: min value window function expression instance.
        """
        return WindowMin(self, expression)

    def sum(self, expression: BaseColumnExpression) -> WindowSum:
        """Apply a sum aggregation expression: get the value of the expression summed over a window.

        Args:
            expression (BaseColumnExpression): expression to take the sum of in the window.

        Returns:
            WindowSum: sum value window function expression instance.
        """
        return WindowSum(self, expression)

    def cume_dist(self) -> CumeDist:
        """Apply a cumulative distribution ranking expression: position of an expression's value in the cumulative
        distribution of the expression normalised between 0 and 1.

        Returns:
            CumeDist: cumulative dist window function expression instance.
        """
        return CumeDist(self)

    def dense_rank(self) -> DenseRank:
        """Apply a dense rank expression to the window. Equal values (in the sort by column(s)) will have the same value,
        the next value in rank after is not skipped in the case of a tie (in contrast to the rank function).

        Returns:
            Rank: dense rank window function expression object.
        """
        return DenseRank(self)

    def ntile(self, n: int) -> NTile:
        """Apply an N tile expression to the window. This will assign in integer label to each row in the window such
        that the window is partitioned into n-many groups in a tiling fashion.

        Args:
            n (int): number of tiles.

        Returns:
            NTile: n tile window function expression object.
        """
        return NTile(self, n)

    def rank(self) -> Rank:
        """Apply a rank expression to the window. Equal values (in the sort by column(s)) will have the same value,
        the next value in rank after is skipped in the case of a tie.

        Returns:
            Rank: rank window function expression object.
        """
        return Rank(self)

    def row_number(self) -> RowNumber:
        """Apply a row number expression to the window. This will return the in-window row number value as a new column.

        Returns:
            RowNumber: row number window function expression object.
        """
        return RowNumber(self)

    def percent_rank(self) -> PercentRank:
        """Apply a percent rank expression to the window. This will return the rank of a row as a number between 0 and 1

        Returns:
            PercentRank: percent rank window function expression object.
        """
        return PercentRank(self)

    def drawdown(self, expression: BaseColumnExpression) -> BaseColumnExpression:
        """Build and apply a drawdown expression to a given column expression.

        Drawdown is the fractional decrease of the current column value from a prior maximum (high watermark).
        It is calculated as follows:
            (val - high_watermark)/(high_watermark)
        This will calculate drawdown for a price series, but not a series of returns.

        Maximum drawdown can be computed from this expression by calling .min() on it.

        Args:
            expression (BaseColumnExpression): expression to compute the drawdown for.

        Returns:
            BaseColumnExpression: column expression object for the drawdown calculation.
        """
        # todo: change back to / when case works with window fns
        return (expression - self.max(expression)) // self.max(expression)

    def frac_diff(self, expression: BaseColumnExpression, offset: Optional[int] = 1):
        """Apply an expression that computes the fractional difference between values in a column displaced by some offset.

        Computed as
            frac_diff = (current - previous)/previous
        The first value in the resulting series will be null.

        For the default offset=1 case, the values
            1, 1.5, 0.75, 1.5
        become
            NULL, 0.5, -0.5, 2

        Args:
            expression (BaseColumnExpression): the expression to compute the fractional difference between rows of.
            offset (Optional[int]): offset between current and previous values in the calculation (default = 1).

        Returns:
            BaseColumnExpression: column expression object for the fractional difference calculation.

        """
        # todo: change back to / when case works with window fns
        return (expression - self.lag(expression, offset)) // self.lag(expression, offset)

    def filter(self, expression: BaseColumnExpression) -> FilteredOver:
        """Apply a filter expression to the window function. The filter will remove rows that evaluate to false and
        they will therefore be ignored in the window function calculation.

        Args:
            expression (BaseColumnExpression): filter expression to use. Must evaluate to a boolean.

        Returns:
            FilteredOver: FilteredOver instance that represents the given OVER with the given filter expression.
        """
        return FilteredOver(self, expression)


class FilteredOver(Over):
    """Class representing an OVER clause with a preceding FILTER(WHERE ...) in a SQL window function specification.

    """

    def __init__(self, over: Over, filter_expr: BaseColumnExpression):
        """Constructor of the FilteredOver class.

        Args:
            over (Over): the Over instance to apply a filter to.
            filter_expr (BaseColumnExpression): the filter expression to apply.
        """

        if filter_expr.get_type() != SqlValType.Boolean:
            raise ValueError(f'Window FILTER expression did not resolve to Boolean. Was {filter_expr.get_type().name}')

        self.filter_expr = filter_expr
        self.over = over
        super().__init__(
            over.partitions,
            over.orders,
            over.frame,
        )

    def get_sql(self) -> str:
        over_str = super().get_sql()
        return f"FILTER(WHERE {self.filter_expr.get_sql()}) {over_str}"

    def filter(self, expression: BaseColumnExpression) -> FilteredOver:
        """Apply another filter expression to the window function. The filter will remove rows that evaluate to false and
        they will therefore be ignored in the window function calculation.
        The given filter will be evaluated &'ed together with prior ones.

        Args:
            expression (BaseColumnExpression): filter expression to use. Must evaluate to a boolean.

        Returns:
            FilteredOver: FilteredOver instance that represents the given OVER with the given filter expression.
        """

        return FilteredOver(
            self.over,
            self.filter_expr & expression
        )


def window(
        groups: Optional[Union[Iterable[BaseColumnExpression], BaseColumnExpression]] = None,
        orders: Optional[Union[Iterable[BaseColumnOrdering], BaseColumnOrdering]] = None,
        lower: Optional[int, None] = None,
        upper: Optional[int, None] = 0
) -> Over:
    """Build a window that will be used with window functions.
    Windows are a particular partition, and/or a sliding range of rows around a central row with an optional ordering.
    If no ordering is applied it'll just evaluate in RowID order.

    Once built a window can be used to build window functions by calling methods on the window object such as sum(),
    first() or rank().

    Args:
        groups (Optional[Union[Iterable[BaseColumnExpression], BaseColumnExpression]]): one of either a list of column
            expressions, a single column expression or None. None means there is no partition in the windowing (default).
        orders (Optional[Union[Iterable[BaseColumnOrdering], BaseColumnOrdering]]): one of either a list of column
            expression orderings, a single one or None. None means that the window will be sorted by row number (default).
        lower (Optional[Union[int, None]]): lower (start) limit of the window as a number of rows before the current
            row. If None then the window is unbounded below and has no lower limit, if zero it is the current row (default is None).
        upper (Optional[Union[int, None]]): upper (end) limit of the window as a number of rows after the current row.
            If None then the window is unbounded above and has no upper limit, if 0 it is the current row (default is 0).

    Returns:
        Over: the over instance representing the window defined by the arguments.
    """
    if isinstance(groups, (list, tuple)) and len(groups) > 0:
        partition = WindowPartition(*groups)
    elif groups is not None:
        partition = WindowPartition(groups)
    else:
        partition = None

    if isinstance(orders, (list, tuple)) and len(orders) > 0:
        ordering = WindowOrder(*orders)
    elif orders is not None:
        ordering = WindowOrder(orders)
    else:
        ordering = None

    frame = WindowFrame.create(lower, upper)

    return Over(partition, ordering, frame)
