import pytest
from iguanas.rule_selection import GreedyFilter
from iguanas.metrics import FScore, Precision
import iguanas.utils as utils
import numpy as np
import pandas as pd
import random


@pytest.fixture
def create_data():
    def return_random_num(y, fraud_min, fraud_max, nonfraud_min, nonfraud_max, rand_func):
        data = [rand_func(fraud_min, fraud_max) if i == 1 else rand_func(
            nonfraud_min, nonfraud_max) for i in y]
        return data

    random.seed(0)
    np.random.seed(0)
    y = pd.Series(data=[0]*980 + [1]*20, index=list(range(0, 1000)))
    X_rules = pd.DataFrame(data={
        "Rule1": [0]*980 + [1]*6 + [0] * 14,
        "Rule2": [0]*987 + [1]*6 + [0] * 7,
        "Rule3": [0]*993 + [1]*6 + [0] * 1,
        "Rule4": [round(max(i, 0)) for i in return_random_num(y, 0.4, 1, 0.5, 0.6, np.random.uniform)],
        "Rule5": [round(max(i, 0)) for i in return_random_num(y, 0.2, 1, 0, 0.6, np.random.uniform)],
    },
        index=list(range(0, 1000))
    )
    weights = y.apply(lambda x: 10 if x == 1 else 1)
    return X_rules, y, weights


@pytest.fixture
def return_rule_descriptions(create_data):
    X_rules, y, weights = create_data
    f4 = FScore(beta=4)
    rd_no_weight = utils.return_binary_pred_perf_of_set(
        y_true=y, y_preds=X_rules, y_preds_columns=X_rules.columns, metric=f4.fit)
    rd_weight = utils.return_binary_pred_perf_of_set(
        y_true=y, y_preds=X_rules, y_preds_columns=X_rules.columns, sample_weight=weights, metric=f4.fit)
    return rd_no_weight, rd_weight


@pytest.fixture
def instantiate_GreedyFilter(return_rule_descriptions):
    rd_no_weight, rd_weight = return_rule_descriptions
    f4 = FScore(beta=4)
    p = Precision()
    gf_w_rd_no_weight = GreedyFilter(
        metric=f4.fit,
        sorting_metric=p.fit,
        rule_descriptions=rd_no_weight,
    )
    gf_w_rd_weight = GreedyFilter(
        metric=f4.fit,
        sorting_metric=p.fit,
        rule_descriptions=rd_weight,
    )
    gf_wo_rd_no_weight = GreedyFilter(
        metric=f4.fit,
        sorting_metric=p.fit
    )
    gf_wo_rd_weight = GreedyFilter(
        metric=f4.fit,
        sorting_metric=p.fit
    )
    return gf_w_rd_no_weight, gf_w_rd_weight, gf_wo_rd_no_weight, gf_wo_rd_weight


@ pytest.fixture
def expected_results_GreedyFilter(create_data):
    X_rules, _, _ = create_data
    expected_results = [
        X_rules[['Rule1', 'Rule2', 'Rule3']],
        X_rules[['Rule1', 'Rule2', 'Rule3', 'Rule5']]
    ]
    return expected_results


@pytest.fixture
def expected_scores():
    expected_scores = [0.9053254437869824, 0.9486607142857143] * 2
    return expected_scores


@ pytest.fixture
def expected_results_return_performance_top_n():
    top_n_no_weight = pd.DataFrame(
        {'Precision': {1: 1.0, 2: 1.0, 3: 1.0, 4: 0.09803921568627451, 5: 0.02},
         'Recall': {1: 0.3, 2: 0.6, 3: 0.9, 4: 1.0, 5: 1.0},
         'PercDataFlagged': {1: 0.006, 2: 0.012, 3: 0.018, 4: 0.204, 5: 1.0},
         'Metric': {1: 0.31288343558282206, 2: 0.6144578313253012, 3: 0.9053254437869824, 4: 0.648854961832061, 5: 0.25757575757575757}}
    )
    top_n_weight = pd.DataFrame(
        {'Precision': {1: 1.0, 2: 1.0, 3: 1.0, 4: 0.5208333333333334, 5: 0.1694915254237288},
         'Recall': {1: 0.3, 2: 0.6, 3: 0.9, 4: 1.0, 5: 1.0},
         'PercDataFlagged': {1: 0.006, 2: 0.012, 3: 0.018, 4: 0.204, 5: 1.0},
         'Metric': {1: 0.31288343558282206, 2: 0.6144578313253012, 3: 0.9053254437869824, 4: 0.9486607142857143, 5: 0.776255707762557}}
    )
    top_n_no_weight.index.name = 'Top n rules'
    top_n_weight.index.name = 'Top n rules'
    return top_n_no_weight, top_n_weight


def test_fit(create_data, instantiate_GreedyFilter, expected_results_GreedyFilter, expected_scores):
    X_rules, y, weights = create_data
    expected_results_GreedyFilter = expected_results_GreedyFilter
    expected_scores = expected_scores
    gf_w_rd_no_weight, gf_w_rd_weight, gf_wo_rd_no_weight, gf_wo_rd_weight = instantiate_GreedyFilter
    # Without weight, with rule_descriptions
    gf_w_rd_no_weight.fit(X_rules=X_rules, y=y)
    assert gf_w_rd_no_weight.rules_to_keep == \
        expected_results_GreedyFilter[0].columns.tolist()
    assert gf_w_rd_no_weight.score == expected_scores[0]
    # Without weight, without rule_descriptions
    gf_wo_rd_no_weight.fit(X_rules=X_rules, y=y)
    assert gf_wo_rd_no_weight.rules_to_keep == \
        expected_results_GreedyFilter[0].columns.tolist()
    assert gf_wo_rd_no_weight.score == expected_scores[0]
    # With weight, with rule_descriptions
    gf_w_rd_weight.fit(X_rules=X_rules, y=y, sample_weight=weights)
    assert gf_w_rd_weight.rules_to_keep == \
        expected_results_GreedyFilter[1].columns.tolist()
    assert gf_w_rd_weight.score == expected_scores[1]
    # With weight, without rule_descriptions
    gf_wo_rd_weight.fit(X_rules=X_rules, y=y, sample_weight=weights)
    assert gf_wo_rd_weight.rules_to_keep == \
        expected_results_GreedyFilter[1].columns.tolist()
    assert gf_wo_rd_weight.score == expected_scores[1]


def test_transform(create_data, instantiate_GreedyFilter):
    X_rules, _, _ = create_data
    gf, _, _, _ = instantiate_GreedyFilter
    gf.rules_to_keep = ['Rule1']
    X_rules_filtered = gf.transform(X_rules)
    assert (all(X_rules_filtered == X_rules['Rule1'].to_frame()))


def test_fit_transform(create_data, instantiate_GreedyFilter,
                       expected_results_GreedyFilter, expected_scores):
    X_rules, y, weights = create_data
    expected_results_GreedyFilter = expected_results_GreedyFilter
    expected_scores = expected_scores
    gf_w_rd_no_weight, gf_w_rd_weight, gf_wo_rd_no_weight, gf_wo_rd_weight = instantiate_GreedyFilter
    # Without weight, with rule_descriptions
    X_rules_filtered = gf_w_rd_no_weight.fit_transform(
        X_rules=X_rules, y=y)
    assert gf_w_rd_no_weight.rules_to_keep == expected_results_GreedyFilter[0].columns.tolist(
    )
    assert all(X_rules_filtered == expected_results_GreedyFilter[0])
    assert gf_w_rd_no_weight.score == expected_scores[0]
    assert gf_w_rd_no_weight.rule_descriptions.index.tolist(
    ) == gf_w_rd_no_weight.rules_to_keep
    # Without weight, without rule_descriptions
    X_rules_filtered = gf_wo_rd_no_weight.fit_transform(
        X_rules=X_rules, y=y)
    assert gf_wo_rd_no_weight.rules_to_keep == expected_results_GreedyFilter[0].columns.tolist(
    )
    assert all(X_rules_filtered == expected_results_GreedyFilter[0])
    assert gf_wo_rd_no_weight.score == expected_scores[0]
    assert gf_wo_rd_no_weight.rule_descriptions is None
    # With weight, with rule_descriptions
    X_rules_filtered = gf_w_rd_weight.fit_transform(
        X_rules=X_rules, y=y, sample_weight=weights)
    assert gf_w_rd_weight.rules_to_keep == expected_results_GreedyFilter[1].columns.tolist(
    )
    assert all(X_rules_filtered == expected_results_GreedyFilter[1])
    assert gf_w_rd_weight.score == expected_scores[1]
    assert gf_w_rd_weight.rule_descriptions.index.tolist(
    ) == gf_w_rd_weight.rules_to_keep
    # With weight, without rule_descriptions
    X_rules_filtered = gf_wo_rd_weight.fit_transform(
        X_rules=X_rules, y=y, sample_weight=weights)
    assert gf_wo_rd_weight.rules_to_keep == expected_results_GreedyFilter[1].columns.tolist(
    )
    assert all(X_rules_filtered == expected_results_GreedyFilter[1])
    assert gf_wo_rd_weight.score == expected_scores[1]
    assert gf_wo_rd_weight.rule_descriptions is None


def test_sort_rules(create_data, instantiate_GreedyFilter):
    p = Precision()
    f4 = FScore(beta=4)
    X_rules, y, _ = create_data
    gf_w_rd_no_weight, _, _, _ = instantiate_GreedyFilter
    sorted_rules = gf_w_rd_no_weight._sort_rules(
        X_rules, y, None, p.fit, f4.fit)
    assert sorted_rules == ['Rule1', 'Rule2', 'Rule3', 'Rule5', 'Rule4']


def test_return_performance_top_n(create_data, instantiate_GreedyFilter, expected_results_return_performance_top_n):
    X_rules, y, weights = create_data
    gf_w_rd_no_weight, gf_w_rd_weight, _, _ = instantiate_GreedyFilter
    expected_results = expected_results_return_performance_top_n
    expected_top_n_rules = {
        1: ['Rule1'],
        2: ['Rule1', 'Rule2'],
        3: ['Rule1', 'Rule2', 'Rule3'],
        4: ['Rule1', 'Rule2', 'Rule3', 'Rule4'],
        5: ['Rule1', 'Rule2', 'Rule3', 'Rule4', 'Rule5']
    }
    f4 = FScore(beta=4)
    for i, (gf, w) in enumerate(zip([gf_w_rd_no_weight, gf_w_rd_weight], [None, weights])):
        sorted_rules = gf.rule_descriptions.index.tolist()
        top_n_rule_descriptions, top_n_rules = gf._return_performance_top_n(
            sorted_rules, X_rules, y, w, f4.fit, 0)
        assert all(top_n_rule_descriptions == expected_results[i])
        assert top_n_rules == expected_top_n_rules


def test_return_top_rules_by_opt_func(instantiate_GreedyFilter,
                                      expected_results_return_performance_top_n,
                                      expected_results_GreedyFilter,
                                      return_rule_descriptions,
                                      expected_scores):
    gf, _, _, _ = instantiate_GreedyFilter
    top_n_list = expected_results_return_performance_top_n
    rule_descriptions_list = return_rule_descriptions
    rule_descriptions_list = [rd.sort_values('Precision', ascending=False)
                              for rd in rule_descriptions_list]
    expected_results = expected_results_GreedyFilter
    expected_scores = expected_scores
    for i, (top_n, rule_descriptions) in enumerate(zip(top_n_list, rule_descriptions_list)):
        rules_to_keep, score = gf._return_top_rules_by_opt_func(
            top_n, rule_descriptions.index.tolist())
        assert rules_to_keep == expected_results[i].columns.tolist()
        assert score == expected_scores[i]
