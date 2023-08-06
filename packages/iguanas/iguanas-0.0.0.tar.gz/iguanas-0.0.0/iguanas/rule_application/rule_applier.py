"""Applies rules in the standard Iguanas string format."""
import pandas as pd
import numpy as np
import iguanas.utils as utils
from typing import Dict, Union
from iguanas.utils.types import KoalasDataFrame, KoalasSeries, PandasDataFrame,\
    PandasSeries
from iguanas.utils.typing import KoalasDataFrameType, KoalasSeriesType,\
    PandasDataFrameType, PandasSeriesType


class RuleApplier:
    """
    Applies rules (stored in the standard Iguanas string format) to a dataset.

    Parameters
    ----------
    rule_strings : Dict[str, str]
        Set of rules defined using the standard Iguanas string format 
        (values) and their names (keys).
    metric : Callable, optional
        A function/method which calculates a custom performance metric (e.g.
        Fbeta score) for each rule. Defaults to None.

    Attributes
    ----------
    rule_descriptions : PandasDataFrameType
        Contains the logic of the rules and their performance metrics as 
        applied to the dataset.        
    """

    def __init__(self, rule_strings: Dict[str, str], metric=None):
        self.metric = metric
        self.rule_strings = rule_strings
        self.unapplied_rule_names = []

    def transform(self, X: Union[PandasDataFrameType, KoalasDataFrameType], y=None,
                  sample_weight=None) -> Union[PandasDataFrameType, KoalasDataFrameType]:
        """
        Applies the set of rules to a dataset, `X`. If `y` is provided, the 
        performance metrics for each rule will also be calculated.

        Parameters
        ----------
        X : Union[PandasDataFrameType, KoalasDataFrameType]
            The feature set on which the rules should be applied.            
        y : Union[PandasSeriesType, KoalasSeriesType], optional
            The target column. Defaults to None.
        sample_weight : Union[PandasSeriesType, KoalasSeriesType], optional 
            Record-wise weights to apply. Defaults to None.

        Returns
        -------
            Union[PandasDataFrameType, KoalasDataFrameType]
                The binary columns of the rules.
        """
        utils.check_allowed_types(X, 'X', [PandasDataFrame, KoalasDataFrame])
        if y is not None:
            utils.check_allowed_types(y, 'y', [PandasSeries, KoalasSeries])
        if sample_weight is not None:
            utils.check_allowed_types(
                sample_weight, 'sample_weight', [PandasSeries, KoalasSeries])
        X_rules = self._get_X_rules(X)
        rule_strings_list = list(self.rule_strings.values())
        if (y is None and self.metric is not None) or (y is not None):
            rule_descriptions = utils.return_rule_descriptions_from_X_rules(
                X_rules=X_rules, X_rules_cols=X_rules.columns, y_true=y,
                sample_weight=sample_weight, metric=self.metric
            )
            rule_descriptions['Logic'] = rule_strings_list
            rule_descriptions['nConditions'] = list(map(
                utils.count_rule_conditions, rule_strings_list))
            self.rule_descriptions, X_rules = utils.sort_rule_dfs_by_opt_metric(
                rule_descriptions, X_rules)
        return X_rules

    def _get_X_rules(self, X: Union[PandasDataFrameType, KoalasDataFrameType]) -> Union[
            PandasDataFrameType, KoalasDataFrameType]:
        """
        Returns the binary columns of the list of rules applied to the 
        dataset `X`.
        """

        X_rules_list = []
        for rule_name, rule_string in self.rule_strings.items():
            try:
                X_rule = eval(rule_string)
            except KeyError as e:
                raise KeyError(
                    f'Feature {e} in rule `{rule_name}` not found in `X`')
            if utils.is_type(X_rule, (PandasSeries, KoalasSeries)):
                X_rule = X_rule.fillna(False).astype(int)
                X_rule.name = rule_name
            elif isinstance(X_rule, np.ndarray):
                X_rule = X_rule.astype(int)
            X_rules_list.append(X_rule)
        if isinstance(X_rules_list[0], np.ndarray):
            X_rules = pd.DataFrame(np.asarray(X_rules_list)).T
            X_rules.columns = list(self.rule_strings.keys())
        else:
            X_rules = utils.concat(X_rules_list, axis=1, sort=False)
        X_rules.index = X.index
        return X_rules
