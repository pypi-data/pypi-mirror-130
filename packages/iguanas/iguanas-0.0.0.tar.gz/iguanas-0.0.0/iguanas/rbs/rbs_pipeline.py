"""Defines a Rules-Based System (RBS) pipeline."""
import pandas as pd
import numpy as np
import iguanas.utils as utils
from iguanas.utils.types import PandasDataFrame, PandasSeries
from iguanas.utils.typing import PandasDataFrameType, PandasSeriesType
from typing import List, Callable


class RBSPipeline:
    """
    A pipeline with each stage giving a decision - either 0 or 1 (corresponding 
    to the binary target). Each stage is configured with a set of rules which, 
    if any of them trigger, mark the relevant records with that decision.

    Parameters
    ----------
    config : List[dict]
        The pipeline configuration, where each element aligns to a stage in
        the pipeline. Each element is a dictionary, where the key is the
        decision made at that stage (either 0 or 1) and the value is a list
        of the rules that must trigger to give that decision.
    final_decision : int
        The final decision to apply if no rules are triggered. Must be 
        either 0 or 1.
    metric : Callable
        The method/function used to calculate the performance metric of the 
        pipeline (e.g. F1 score).

    Raises
    ------
    ValueError
        `config` must be a list.
    ValueError
        `final_decision` must be either 0 or 1.

    Attributes
    ----------
    score : float 
        The result of the `metric` function when the pipeline is applied.
    conf_matrix : PandasDataFrameType 
        The confusion matrix for the applied pipeline. Only generated after 
        running `calc_performance`.
    conf_matrix_weighted : PandasDataFrameType 
        The confusion matrix for the applied pipeline. Only generated after 
        running `calc_performance` and when `sample_weight` is provided.
    pipeline_perf : PandasDataFrameType 
        The performance (precision, recall, percentage of data flagged) of each 
        decision made by the pipeline. Only generated after running 
        `calc_performance`.
    """

    def __init__(self, config: List[dict], final_decision: int,
                 metric: Callable) -> None:
        if not isinstance(config, list):
            raise ValueError('`config` must be a list')
        if final_decision not in [0, 1]:
            raise ValueError('`final_decision` must be either 0 or 1')
        self.config = config
        self.final_decision = final_decision
        self.metric = metric

    def predict(self, X_rules: PandasDataFrameType, y: PandasSeriesType,
                sample_weight=None) -> PandasSeriesType:
        """
        Applies the pipeline to the given dataset.

        Parameters
        ----------
        X_rules : PandasDataFrameType
            Dataset of each applied rule.
        y : PandasSeriesType
            The target.
        sample_weight : PandasSeriesType, optional
            Record-wise weights to apply. Defaults to None. Defaults to 
            None.        

        Returns
        -------
            PandasSeriesType
                The prediction of the pipeline.        
        """
        utils.check_allowed_types(X_rules, 'X_rules', [PandasDataFrame])
        utils.check_allowed_types(y, 'y', [PandasSeries])
        if sample_weight is not None:
            utils.check_allowed_types(
                sample_weight, 'sample_weight', [PandasSeries])
        num_rows = len(X_rules)
        stage_level_preds = self._get_stage_level_preds(X_rules, self.config)
        y_pred = self._get_pipeline_pred(stage_level_preds, num_rows)
        self.score = self.metric(
            y_preds=y_pred, y_true=y, sample_weight=sample_weight
        )
        return y_pred

    def calc_performance(self, y_true: PandasSeriesType, y_pred: PandasSeriesType,
                         sample_weight=None) -> None:
        """
        Calculates the confusion matrices (non-weighted and weighted, if 
        provided) and overall performance of the pipeline.

        Note that for the confusion matrices, the index shows the 
        predicted class; the column shows the actual class.

        Parameters
        ----------
        y_true : PandasSeriesType
            The target.
        y_pred : PandasSeriesType
            The RBS pipeline prediction.
        sample_weight : PandasSeriesType, optional
            Record-wise weights to apply. Defaults to None. Defaults to 
            None. 
        """

        # Get confusion matrix (number of events)
        self.conf_matrix = utils.return_conf_matrix(
            y_true=y_true, y_pred=y_pred, sample_weight=None
        )
        # Get confusion matrix using sample_weight (if given)
        if sample_weight is not None:
            self.conf_matrix_weighted = utils.return_conf_matrix(
                y_true=y_true, y_pred=y_pred, sample_weight=sample_weight
            )
        # Get overall pipeline perf
        perf_1 = utils.return_binary_pred_perf_of_set(
            y_true=y_true, y_preds=y_pred, y_preds_columns=[1],
            sample_weight=sample_weight,
        )
        perf_0 = utils.return_binary_pred_perf_of_set(
            y_true=-(y_true-1), y_preds=-(y_pred-1), y_preds_columns=[0],
            sample_weight=sample_weight,
        )
        self.pipeline_perf = pd.concat(
            [perf_1, perf_0], axis=0).drop(['Metric'], axis=1)

    @staticmethod
    def _get_stage_level_preds(X_rules: PandasDataFrameType,
                               config: List[dict]) -> PandasDataFrameType:
        """Returns the predictions for each stage in the pipeline"""

        rules = X_rules.columns.tolist()
        stage_level_preds = []
        for i, stage in enumerate(config):
            decision = list(stage.keys())[0]
            stage_rules = list(stage.values())[0]
            stage_rules_present = [
                rule for rule in stage_rules if rule in rules]
            if not stage_rules_present:
                continue
            y_pred_stage = (
                X_rules[stage_rules_present].sum(1) > 0).astype(int)
            if decision == 0:
                y_pred_stage = -y_pred_stage
            y_pred_stage.name = f'Stage={i}, Decision={decision}'
            stage_level_preds.append(y_pred_stage)
        if not stage_level_preds:
            return None
        else:
            stage_level_preds = pd.concat(stage_level_preds, axis=1)
            return stage_level_preds

    def _get_pipeline_pred(self, stage_level_preds: PandasDataFrameType,
                           num_rows: int) -> PandasSeriesType:
        """Returns the predictions of the pipeline"""

        if stage_level_preds is None:
            return np.ones(num_rows) * self.final_decision
        for stage_idx in range(0, len(stage_level_preds.columns)):
            if stage_idx == 0:
                y_pred = stage_level_preds.iloc[:, stage_idx]
            else:
                y_pred = (
                    (y_pred == 0).astype(int) * stage_level_preds.iloc[:, stage_idx]) + y_pred
        y_pred = ((y_pred == 0).astype(int) * self.final_decision) + y_pred
        y_pred = (y_pred > 0).astype(int)
        return y_pred
