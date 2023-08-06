"""Filters rules based on performance metrics."""
from iguanas.rule_selection._base_filter import _BaseFilter
from typing import Callable
from iguanas.utils.typing import PandasDataFrameType

FILTERING_FUNCTIONS = {
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x <= y,
    '<=': lambda x, y: x <= y
}


class SimpleFilter(_BaseFilter):
    """
    Filter rules based on a metric.

    Parameters
    ----------
    threshold : float
        The threshold at which the rules are filtered.
    operator : str
        The operator used to filter the rules. Can be one of the following: 
        '>', '>=', '<', '<='
    metric : Callable
        The method/function which calculates the metric by which the rules are
        filtered.
    rule_descriptions : PandasDataFrameType, optional
        The standard performance metrics dataframe associated with the 
        rules. Provide if you need this dataframe filtered in addition to 
        `X_rules`. Defaults to None.    

    Attributes
    ----------
    rules_to_keep : List[str]
        List of rules which remain after the filter has been applied.
    """

    def __init__(self,
                 threshold: float,
                 operator: str,
                 metric: Callable,
                 rule_descriptions=None):
        if operator not in ['>', '>=', '<', '<=']:
            raise ValueError("`operator` must be '>', '>=', '<' or '<='")
        self.threshold = threshold
        self.operator = operator
        self.metric = metric
        _BaseFilter.__init__(self, rule_descriptions)

    def fit(self, X_rules: PandasDataFrameType, y=None, sample_weight=None) -> None:
        """
        Calculates the rules remaining after the filter has been applied.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            The binary columns of the rules applied to a dataset.
        y : PandasSeriesType, optional
            The binary target column. Not required if `rule_descriptions` is 
            given. Defaults to None.
        sample_weight : PandasSeriesType, optional
            Row-wise weights to apply. Defaults to None.
        """

        metrics = self.metric(X_rules, y, sample_weight)
        filter_func = FILTERING_FUNCTIONS[self.operator]
        mask = filter_func(metrics, self.threshold)
        self.rules_to_keep = X_rules.columns[mask].tolist()
