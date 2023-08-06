"""
Base rule filter class. Main filter classes inherit from this one.
"""
from iguanas.utils.typing import PandasDataFrameType


class _BaseFilter:
    """
    Base rule filter class. Main filter classes inherit from this one.

    Parameters
    ----------
    rule_descriptions : PandasDataFrameType, optional
        The standard performance metrics dataframe associated with the 
        rules. Provide if you need this dataframe filtered in addition to 
        `X_rules`. Defaults to None.    
    """

    def __init__(self, rule_descriptions) -> None:
        self.rule_descriptions = rule_descriptions
        self.rules_to_keep = []

    def transform(self, X_rules: PandasDataFrameType) -> PandasDataFrameType:
        """
        Applies the filter to the given dataset.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            The binary columns of the rules applied to a dataset.

        Returns
        -------
        PandasDataFrameType
            The binary columns of the filtered rules.
        """

        X_rules = X_rules[self.rules_to_keep]
        if self.rule_descriptions is not None:
            self.rule_descriptions = self.rule_descriptions.loc[self.rules_to_keep]
        return X_rules

    def fit_transform(self,
                      X_rules: PandasDataFrameType,
                      y=None,
                      sample_weight=None) -> PandasDataFrameType:
        """
        Fits then applies the filter to the given dataset.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            The binary columns of the rules applied to a dataset.
        y : PandasSeriesType, optional
            The target (if relevant). Defaults to None.
        sample_weight : PandasSeriesType, optional
            Row-wise weights to apply. Defaults to None.

        Returns
        -------
        PandasDataFrameType
            The binary columns of the filtered rules.
        """

        self.fit(X_rules=X_rules, y=y, sample_weight=sample_weight)
        return self.transform(X_rules=X_rules)
