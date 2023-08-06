import pytest
import pandas as pd
import numpy as np
from iguanas.rbs import RBSPipeline
from iguanas.metrics.classification import FScore


@pytest.fixture
def _create_data():
    X = pd.DataFrame({
        'Approve1': [1, 0, 0, 0, 0],
        'Approve2': [0, 1, 0, 0, 0],
        'Decline': [1, 1, 1, 0, 0],
        'Approve3': [1, 1, 1, 1, 0],
    })
    y = pd.Series([1, 0, 1, 0, 0])
    return X, y


@pytest.fixture
def _instantiate():
    f1 = FScore(beta=1)
    config = [
        {0: ['Approve1', 'Approve2']},
        {1: ['Decline']},
        {0: ['Approve3']}
    ]
    rbsp = RBSPipeline(
        config=config,
        final_decision=1,
        metric=f1.fit
    )
    return rbsp


def test_predict(_create_data, _instantiate):
    y_pred_exp = pd.Series([0, 0, 1, 0, 1])
    X, y = _create_data
    rbsp = _instantiate
    y_pred = rbsp.predict(X, y)
    assert all(y_pred_exp == y_pred)
    assert rbsp.score == 0.5


def test_get_stage_level_preds(_create_data, _instantiate):
    config = [
        {0: ['Approve1', 'Approve2']},
        {1: ['Decline']},
        {0: ['Approve3']}
    ]
    exp_results = pd.DataFrame([
        [-1, 1, -1],
        [-1, 1, -1],
        [0, 1, -1],
        [0, 0, -1],
        [0, 0, 0]
    ],
        columns=['Stage=0, Decision=0', 'Stage=1, Decision=1', 'Stage=2, Decision=0'])
    X, _ = _create_data
    rbsp = _instantiate
    stage_level_preds = rbsp._get_stage_level_preds(X_rules=X, config=config)
    assert all(stage_level_preds == exp_results)


def test_get_pipeline_pred(_instantiate):
    y_pred_exp = pd.Series([0, 0, 1, 0, 1])
    stage_level_preds = pd.DataFrame([
        [-1, 1, -1],
        [-1, 1, -1],
        [0, 1, -1],
        [0, 0, -1],
        [0, 0, 0]
    ],
        columns=['Stage=0, Decision=0', 'Stage=1, Decision=1', 'Stage=2, Decision=0'])
    rbsp = _instantiate
    y_pred = rbsp._get_pipeline_pred(stage_level_preds, 5)
    assert all(y_pred == y_pred_exp)


def test_calc_performance(_create_data, _instantiate):
    exp_conf_mat = np.array([
        [1, 1],
        [1, 2]
    ])
    exp_pipeline_perf = np.array([
        [0.5, 0.5, 0.4],
        [0.66666667, 0.66666667, 0.6]
    ])
    X, y = _create_data
    rbsp = _instantiate
    y_pred = rbsp.predict(X, y)
    rbsp.calc_performance(y, y_pred, None)
    np.testing.assert_array_almost_equal(rbsp.conf_matrix.values, exp_conf_mat)
    np.testing.assert_array_almost_equal(
        rbsp.pipeline_perf.values, exp_pipeline_perf)


def test_errors(_create_data):
    X, y = _create_data
    f1 = FScore(1)
    with pytest.raises(ValueError, match='`config` must be a list'):
        rbsp = RBSPipeline(
            config={},
            final_decision=0,
            metric=f1.fit
        )
    with pytest.raises(ValueError, match='`final_decision` must be either 0 or 1'):
        rbsp = RBSPipeline(
            config=[],
            final_decision=2,
            metric=f1.fit
        )
    with pytest.raises(TypeError, match='`X_rules` must be a pandas.core.frame.DataFrame. Current type is str.'):
        rbsp = RBSPipeline(
            config=[],
            final_decision=0,
            metric=f1.fit
        )
        rbsp.predict('X', y)
    with pytest.raises(TypeError, match='`y` must be a pandas.core.series.Series. Current type is str.'):
        rbsp.predict(X, 'y')
