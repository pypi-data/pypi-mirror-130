"""Filters rules using a greedy-type methodology"""
from iguanas.rule_selection._base_filter import _BaseFilter
import numpy as np
import pandas as pd
import iguanas.utils as utils
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Callable, Tuple
import matplotlib.ticker as ticker
import math
from iguanas.utils.typing import PandasDataFrameType, PandasSeriesType


class GreedyFilter(_BaseFilter):
    """
    Sorts rules by a given metric, calculates the combined performance of the
    top n rules, then filters to the rules which give the best combined 
    performance.

    Parameters
    ----------
    metric : Callable
        The method/function used to calculate the performance of the top n 
        rules (e.g. Fbeta score).
    sorting_metric : Callable
        The method/function used calculate the performance metric by which the 
        rules are sorted.
    rule_descriptions : PandasDataFrameType, optional
        The standard performance metrics dataframe associated with the 
        rules. Provide if you need this dataframe filtered in addition to 
        `X_rules`. Defaults to None.    
    verbose : int, optional
        Controls the verbosity - the higher, the more messages. >0 : shows the
        progress of the filtering process. Defaults to 0.        

    Attributes
    ----------
    rules_to_keep : List[str]
        List of rules which give the best combined performance.
    score : float
        The combined performance (i.e. the value of `metric`) of the rules 
        which give the best combined performance.
    """

    def __init__(self,
                 metric: Callable,
                 sorting_metric: Callable,
                 rule_descriptions=None,
                 verbose=0):

        self.metric = metric
        self.sorting_metric = sorting_metric
        _BaseFilter.__init__(self, rule_descriptions)
        self.verbose = verbose

    def fit(self, X_rules: PandasDataFrameType, y=PandasSeriesType,
            sample_weight=None) -> None:
        """
        Sorts rules by a given metric, calculates the combined performance of
        the top n rules, then calculates the rules which give the best combined
        performance.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            The binary columns of the rules applied to a dataset.
        y : PandasSeriesType
            The binary target column.
        sample_weight : PandasSeriesType, optional
            Row-wise weights to apply. Defaults to None.
        """

        sorted_rules = self._sort_rules(
            X_rules=X_rules, y=y, sample_weight=sample_weight,
            sorting_metric=self.sorting_metric,
            metric=self.metric
        )
        self.sorted_rules = sorted_rules
        self.top_n_rule_descriptions, self.top_n_rules = self._return_performance_top_n(
            sorted_rules=sorted_rules, X_rules=X_rules, y=y,
            sample_weight=sample_weight, metric=self.metric,
            verbose=self.verbose)
        self.rules_to_keep, self.score = self._return_top_rules_by_opt_func(
            self.top_n_rule_descriptions, sorted_rules)

    def plot_top_n_performance_on_train(self,
                                        figsize=(10, 5),
                                        title='`metric` performance of the top n rules on the training set') -> sns.lineplot:
        """
        Plot the combined performance of the top n rules (as calculated using 
        the `.fit()` method).

        Parameters
        ----------
        figsize : Tuple[int, int], optional
            Defines the size of the plot (length, height). Defaults to (10, 5).
        verbose : int, optional
            Controls the verbosity - the higher, the more messages. >0 : shows
            the progress of calculating the combined performance of the top n
            rules. Defaults to 0.
        title : str, optional
            The plot title. Defaults to '`metric` performance of the top n
            rules on the training set'

        Returns
        -------
        sns.lineplot
            Shows the combined performance of the top n rules.
        """

        self._plot_performance(
            data=self.top_n_rule_descriptions['Metric'].to_frame(),
            title=title,
            figsize=figsize
        )

    def plot_top_n_performance(self, X_rules: PandasDataFrameType,
                               y: PandasSeriesType,
                               sample_weight=None,
                               figsize=(10, 5),
                               verbose=0,
                               title='`metric` performance of the top n rules') -> sns.lineplot:
        """
        Plot the combined performance of the top n rules (as calculated using 
        the `.fit()` method) using the provided rule binary columns.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            The binary columns of the rules applied to a dataset.
        y : PandasSeriesType
            The binary target column.
        sample_weight : PandasSeriesType, optional
            Row-wise weights to apply. Defaults to None.
        figsize : Tuple[int, int], optional
            Defines the size of the plot (length, height). Defaults to (10, 5).
        verbose : int, optional
            Controls the verbosity - the higher, the more messages. >0 : shows
            the progress of calculating the combined performance of the top n
            rules. Defaults to 0.
        title : str, optional
            The plot title. Defaults to '`metric` performance of the top n
            rules'

        Returns
        -------
        sns.lineplot
            Shows the combined performance of the top n rules, calculated using 
            the provided rule binary columns.
        """
        sorted_rules = list(self.top_n_rules.values())[-1]
        top_n_rule_descriptions, _ = self._return_performance_top_n(
            sorted_rules=sorted_rules, X_rules=X_rules, y=y,
            sample_weight=sample_weight, metric=self.metric,
            verbose=verbose
        )
        self._plot_performance(
            data=top_n_rule_descriptions['Metric'].to_frame(),
            title=title, figsize=figsize
        )

    def _sort_rules(self,
                    X_rules: PandasDataFrameType,
                    y: PandasSeriesType, sample_weight: PandasSeriesType,
                    sorting_metric: Callable,
                    metric: Callable) -> List[str]:
        """
        Sorts the rule set in descending order by the result of the given 
        `sorting_metric`, then `metric`.
        """

        X_rules_perf = pd.DataFrame({
            'SortingMetric': sorting_metric(X_rules, y, sample_weight),
            'CombinedMetric': metric(X_rules, y, sample_weight),
            'Rule': X_rules.columns.tolist()
        })
        X_rules_perf.sort_values(
            by=['SortingMetric', 'CombinedMetric', 'Rule'], ascending=[False, False, True], inplace=True
        )
        self.X_rules_perf = X_rules_perf
        sorted_rules = X_rules_perf['Rule'].tolist()
        return sorted_rules

    @staticmethod
    def _return_performance_top_n(sorted_rules: list,
                                  X_rules: PandasDataFrameType, y: PandasSeriesType,
                                  sample_weight: PandasSeriesType,
                                  metric: Callable,
                                  verbose: int) -> Tuple[PandasDataFrameType, dict]:
        """
        Sorts rules by a given metric, calculates the combined performance
        of the top n rules
        """

        if verbose > 0:
            print('--- Calculating performance of top n rules ---')
        top_n_rule_descriptions_list = []
        top_n_rules = {}
        X_rules = X_rules.reindex(sorted_rules, axis=1)
        rule_range = utils.return_progress_ready_range(
            verbose=verbose, range=range(1, len(sorted_rules) + 1))
        for n in rule_range:
            top_n_X_rules = X_rules.iloc[:, :n]
            top_n_rules[n] = top_n_X_rules.columns.tolist()
            top_n_combined = np.bitwise_or.reduce(top_n_X_rules.values, axis=1)
            top_n_rule_descriptions_list.append(utils.return_binary_pred_perf_of_set(
                y_true=y, y_preds=top_n_combined, y_preds_columns=[n],
                sample_weight=sample_weight, metric=metric))
        top_n_rule_descriptions = pd.concat(
            top_n_rule_descriptions_list, axis=0)
        top_n_rule_descriptions.index.rename('Top n rules', inplace=True)
        return top_n_rule_descriptions, top_n_rules

    @staticmethod
    def _return_top_rules_by_opt_func(top_n_rule_descriptions: PandasDataFrameType,
                                      sorted_rules: List[str]) -> List[str]:
        """Returns rules which give the top combined performance"""

        idx_max_perf_func = top_n_rule_descriptions['Metric'].idxmax()
        score = top_n_rule_descriptions['Metric'][idx_max_perf_func]
        rules_to_keep = sorted_rules[:idx_max_perf_func]
        return rules_to_keep, score

    @staticmethod
    def _plot_performance(data: PandasDataFrameType, title: str,
                          figsize: Tuple[int, int]) -> sns.lineplot:
        """Creates seaborn lineplot"""

        sns.set_style("whitegrid")
        plt.figure(figsize=figsize)
        ax = sns.lineplot(data=data)
        ax_int = math.ceil(data.index.max()/10)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(ax_int))
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        plt.title(title)
        plt.show()
