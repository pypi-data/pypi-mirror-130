"""
Finds the rule generation/optimisation parameters that produce the
best combined rule performance, using cross validated grid search.
"""
from itertools import product
import pandas as pd
import numpy as np
import iguanas.utils as utils
from iguanas.rule_selection import GreedyFilter
from iguanas.rule_generation import RuleGeneratorDT, RuleGeneratorOpt
from iguanas.rule_optimisation import BayesianOptimiser, DirectSearchOptimiser
from iguanas.rules import Rules
from iguanas.utils.typing import PandasDataFrameType, PandasSeriesType
from typing import List, Union, Callable, Tuple, Dict
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
from iguanas.metrics import Precision
p = Precision()

class _GridSearchCV(Rules):

    """
    Searches across the provided parameter space to find the parameter
    set that produces the best overall rule performance. The overall rule
    performance is calculated using the GreedyFilter class - this sorts the
    rules by the precision then calculates the combined performance of the
    top `n` rules. The maximum combined performance is recorded for that
    parameter set.

    This process is repeated for each stratified fold. The mean performance
    across the folds for each parameter set is recorded, and the parameter
    set that gives the highest mean performance is assumed to be the best.
    The rules are then retrained using these parameters and the complete
    dataset.

    Parameters
    ----------
    rule_class : Union[RuleGeneratorDT, RuleGeneratorOpt, BayesianOptimiser, DirectSearchOptimiser]
        The rule generator or optimiser class that will be used to generate
        or optimise rules.
    param_grid : Dict[str, List]
        A list of parameter values (values) for each parameter (keys) in
        the provided `rule_class`.
    greedy_filter_opt_func : Callable
        The method/function (e.g. Fbeta score) used to calculate the 
        performance of the top n rules when the GreedyFilter class is 
        applied to the rule set.
    cv : int
        The number of stratified folds to create from the dataset.
    refilter : bool, optional
        When refitting the rules using the best parameters and the complete
        dataset, this parameter dictates whether the GreedyFilter class 
        should be applied to the rules post-fitting.
    num_cores : int, optional
        The number of cores to use when iterating through the different 
        folds & parameter sets. Defaults to 1.
    verbose : int, optional
        Controls the verbosity - the higher, the more messages. >0 : shows
        the overall progress of each fold; >1 : gives information on, and
        the progress of, the current parameter set being tested. Note that
        setting `verbose` > 1 only works when `num_cores` = 1. Defaults to 0.

    Attributes
    ----------
    rule_strings : Dict[str, str]
        The rules which achieved the best combined performance, defined using 
        the standard Iguanas string format (values) and their names (keys).
    rule_descriptions : PandasDataFrameType
        A dataframe showing the logic of the rules and their performance 
        metrics on the given dataset.
    param_results_per_fold : PandasDataFrameType
        Shows the best combined rule performance observed for each parameter 
        set and fold.
    param_results_aggregated : PandasDataFrameType
        Shows the mean and the standard deviation of the best combined rule
        performance, calculated across the folds, for each parameter set.
    best_perf : float
        The best combined rule performance achieved.
    best_params : dict
        The parameter set that achieved the best combined rule performance.
    """

    def __init__(self,
                 rule_class: Union[RuleGeneratorDT, RuleGeneratorOpt,
                                   BayesianOptimiser, DirectSearchOptimiser],
                 param_grid: Dict[str, List],
                 greedy_filter_opt_func: Callable,
                 cv: int, refilter=True, num_cores=1, verbose=0):

        self.rule_class = rule_class
        self.greedy_filter_opt_func = greedy_filter_opt_func
        self.num_cores = num_cores
        self.param_grid = param_grid
        self.param_combinations = {i: dict(zip(self.param_grid.keys(), comb)) for i, comb in enumerate(list(
            product(*self.param_grid.values())))}
        self.verbose = verbose
        Rules.__init__(self, rule_strings={}, opt_func=None)
        if self.verbose > 0:
            print(f'{len(self.param_combinations)} unique parameter sets')
        self.cv = cv
        self.refilter = refilter

    def __repr__(self):
        if self.rule_strings:
            return f'GridSearchCV object with {len(self.rule_strings)} rules'
        else:
            return f'GridSearchCV(rule_class={self.rule_class}, param_grid={self.param_grid}, greedy_filter_opt_func={self.greedy_filter_opt_func}, cv={self.cv}, refilter={self.refilter})'

    def fit(self, X: PandasDataFrameType, y: PandasSeriesType, sample_weight=None) -> None:
        """
        Searches across the provided parameter space to find the parameter
        set that produces the best overall rule performance. The overall rule
        performance is calculated using the GreedyFilter class - this sorts the
        rules by the precision then calculates the combined performance of the
        top `n` rules. The maximum combined performance is recorded for that
        parameter set.

        This process is repeated for each stratified fold. The mean performance
        across the folds for each parameter set is recorded, and the parameter
        set that gives the highest mean performance is assumed to be the best.
        The rules are then retrained using these parameters and the complete
        dataset.

        Parameters
        ----------
        X : PandasDataFrameType
            The feature set.
        y : PandasSeriesType
            The binary target column.
        sample_weight : PandasSeriesType, optional
            Row-wise weights to apply. Defaults to None.
        """

        skf = StratifiedKFold(
            n_splits=self.cv,
            random_state=0,
            shuffle=True
        )
        skf.get_n_splits(X, y)
        folds = {i: split for i, split in enumerate(skf.split(X, y))}
        fold_and_param_idxs = list(
            product(folds.keys(), self.param_combinations.keys()))
        fold_and_param_values = list(
            product(folds.values(), self.param_combinations.values()))
        folds_and_params = list(
            zip(fold_and_param_idxs, fold_and_param_values))
        if self.verbose == 1:
            print(
                '--- Fitting and validating rules using folds ---',
            )
        folds_and_params = utils.return_progress_ready_range(
            verbose=self.verbose == 1, range=folds_and_params
        )
        # Fit each param set on each fold and return results
        with Parallel(n_jobs=self.num_cores) as parallel:
            fold_and_param_results = parallel(delayed(self._fit_on_fold_with_params)(
                params, X, y, sample_weight, train_idxs, val_idxs, fold_idx,
                param_set_idx
            ) for (fold_idx, param_set_idx), ((train_idxs, val_idxs), params) in folds_and_params
            )
        folds_perf_list = [fold_perf for fold_perf,
                           _ in fold_and_param_results]
        self.greedy_filters_dict = {fold_param_idxs: greedy_filter for fold_param_idxs, (
            _, greedy_filter) in zip(fold_and_param_idxs, fold_and_param_results)}
        # Drop the train_idxs and val_idxs from the folds_and_params dict
        # and convert to a dataframe
        self.param_results_per_fold = pd.DataFrame(
            {fold_idx: v[1] for fold_idx, v in folds_and_params}).T
        self.param_results_per_fold.index.set_names(
            ['Fold', 'ParamSetIndex'], inplace=True)
        self.param_results_per_fold['Performance'] = folds_perf_list
        self.param_results_aggregated = self._calculate_aggregated_perf(
            param_results_per_fold=self.param_results_per_fold,
            param_combinations=self.param_combinations
        )
        self.best_perf = self.param_results_aggregated[
            'MeanPerformance'].max()
        self.best_index = self.param_results_aggregated[
            'MeanPerformance'].idxmax()
        self.best_params = self.param_combinations[self.best_index]
        if self.verbose > 0:
            print(
                '--- Re-fitting rules using best parameters on full dataset ---',
            )
        # Retrain using best performing params on full dataset
        X_rules, rc = self._train_rules_using_params(
            rule_class=self.rule_class, params=self.best_params, X=X,
            y=y, sample_weight=sample_weight
        )
        # If refilter is True, perform GreedyFilter on rules that were
        # retrained using best parameters and complete dataset
        if self.refilter:
            if self.verbose > 0:
                print(
                    '--- Filtering rules to give best combined performance ---',
                )
            gf = self._fit_greedy_filter(
                greedy_filter_opt_func=self.greedy_filter_opt_func,
                rule_descriptions=rc.rule_descriptions,
                X_rules=X_rules, y=y, sample_weight=sample_weight,
                verbose=self.verbose
            )
            rc.filter_rules(include=gf.rules_to_keep)
        self.rule_strings = rc.rule_strings
        self.opt_func = self.best_params['opt_func']

    def plot_top_n_performance_by_fold(self,
                                       figsize=(10, 5)) -> sns.lineplot:
        """
        Plot the combined performance of the top n rules (as calculated using
        the `.fit()` method) for each parameter set and fold that was used for
        fitting the rules.

        Parameters
        ----------
        figsize : Tuple[int, int], optional
            Defines the size of the plot (length, height). Defaults to (10, 5).

        Returns
        -------
        sns.lineplot
            The combined performance of the top n rules for each parameter set and fold.
        """

        def _plot_performance(param_set_idx, figsize, data):
            sns.set_style("whitegrid")
            plt.figure(figsize=figsize)
            ax = sns.lineplot(data=data)
            ax_int = math.ceil(data.index.max()/10)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(ax_int))
            ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
            plt.title(
                f'Performance of parameter set {param_set_idx} across the {self.cv} validation folds')
            plt.show()

        for param_set_idx in self.param_combinations.keys():
            data_list = []
            for fold_idx in range(self.cv):
                top_n_rule_perf_fold = self.greedy_filters_dict[(
                    fold_idx, param_set_idx)].top_n_rule_descriptions['OptMetric'].to_frame()
                data_list.append(top_n_rule_perf_fold)
            data = pd.concat(data_list, axis=1)
            data.columns = [f'Fold {fold_idx}' for fold_idx in range(self.cv)]
            _plot_performance(param_set_idx, figsize, data)

    def _fit_on_fold_with_params(self, params, X, y, sample_weight,
                                 train_idxs, val_idxs, fold_idx,
                                 param_set_idx) -> Tuple[float, dict, GreedyFilter]:
        """Fits the rules_class on a given fold using the given parameters"""
        if self.verbose > 1:
            print(
                f'--- Fitting rules using parameter set {param_set_idx} and fold {fold_idx} ---')
        X_train, y_train, sample_weight_train, X_val, y_val, sample_weight_val = self._set_up_datasets(
            X=X, y=y, sample_weight=sample_weight, train_idxs=train_idxs, val_idxs=val_idxs)
        X_rules, rc = self._train_rules_using_params(
            rule_class=self.rule_class, params=params, X=X_train,
            y=y_train, sample_weight=sample_weight_train
        )
        rule_descriptions = rc.rule_descriptions
        if (len(X_train.index) != len(X_val.index)) or any(X_train.index != X_val.index):
            X_rules = rc.transform(
                X=X_val, y=y_val, sample_weight=sample_weight_val)
            rule_descriptions = rc.rule_descriptions
        greedy_filterer = self._fit_greedy_filter(
            greedy_filter_opt_func=self.greedy_filter_opt_func,
            rule_descriptions=rule_descriptions,
            X_rules=X_rules,
            y=y_val,
            sample_weight=sample_weight_val,
            verbose=self.verbose,
        )
        params_perf = greedy_filterer.top_n_rule_descriptions['OptMetric'].max(
        )
        rc.filter_rules(include=greedy_filterer.rules_to_keep)
        if self.verbose > 1:
            print(end='\n')
        return params_perf, greedy_filterer

    @staticmethod
    def _set_up_datasets(X: PandasDataFrameType, y: PandasSeriesType, sample_weight: PandasSeriesType,
                         train_idxs: np.array, val_idxs: np.array) -> Tuple[PandasDataFrameType, PandasSeriesType, PandasSeriesType, PandasDataFrameType, PandasSeriesType, PandasSeriesType]:
        """Set up training and validation datasets for each fold"""

        X_train = X.iloc[train_idxs]
        y_train = y.iloc[train_idxs]
        X_val = X.iloc[val_idxs]
        y_val = y.iloc[val_idxs]
        if sample_weight is not None:
            sample_weight_train = sample_weight.iloc[train_idxs]
            sample_weight_val = sample_weight.iloc[val_idxs]
        else:
            sample_weight_train = None
            sample_weight_val = None
        return X_train, y_train, sample_weight_train, X_val, y_val, sample_weight_val

    @staticmethod
    def _calculate_aggregated_perf(param_results_per_fold: PandasDataFrameType,
                                   param_combinations: Dict[int, dict]) -> PandasDataFrameType:
        """
        Calculates the mean and std dev of the overall rule performance across
        the folds for each unique parameter set.
        """

        fold_results_lists = param_results_per_fold.reset_index().groupby('ParamSetIndex')[
            'Performance'].apply(np.array)
        fold_results_lists.name = 'PerformancePerFold'
        mean_performances = fold_results_lists.apply(np.mean)
        mean_performances.name = 'MeanPerformance'
        std_performances = fold_results_lists.apply(np.std)
        std_performances.name = 'StdDevPerformance'
        param_combinations_df = pd.DataFrame(param_combinations).T
        param_results_aggregated = pd.concat([
            param_combinations_df, fold_results_lists, mean_performances,
            std_performances
        ],
            axis=1)
        param_results_aggregated.index.name = 'ParamSetIndex'
        return param_results_aggregated

    @staticmethod
    def _train_rules_using_params(rule_class: Union[RuleGeneratorDT, RuleGeneratorOpt],
                                  params: Dict[str, List], X: PandasDataFrameType, y: PandasSeriesType,
                                  sample_weight: PandasSeriesType) -> Tuple[PandasDataFrameType, Rules]:
        """Train a rule set using the provided parameters"""

        rc = rule_class(**params)
        X_rules = rc.fit(X=X, y=y, sample_weight=sample_weight)
        return X_rules, rc

    @staticmethod
    def _fit_greedy_filter(greedy_filter_opt_func: Union[RuleGeneratorDT, RuleGeneratorOpt],
                           rule_descriptions: PandasDataFrameType,
                           X_rules: PandasDataFrameType,
                           y: PandasSeriesType,
                           sample_weight: PandasSeriesType,
                           verbose: int,
                           ) -> GreedyFilter:
        """Fits the GreedyFilter class to the provided dataset"""

        gf = GreedyFilter(
            combined_metric=greedy_filter_opt_func,
            sorting_metric=p.fit,
            rule_descriptions=rule_descriptions,
#             sorting_col='Precision',            
            verbose=verbose > 1
        )
        gf.fit(X_rules=X_rules, y=y, sample_weight=sample_weight)
        return gf