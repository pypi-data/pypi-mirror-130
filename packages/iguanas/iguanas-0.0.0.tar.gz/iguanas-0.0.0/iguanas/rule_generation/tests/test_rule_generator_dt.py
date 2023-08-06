import pytest
import numpy as np
import pandas as pd
from iguanas.rule_generation import RuleGeneratorDT
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score
from iguanas.metrics.classification import FScore
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
    X = pd.DataFrame(data={
        "num_distinct_txn_per_email_1day": [round(max(i, 0)) for i in return_random_num(y, 2, 1, 1, 2, np.random.normal)],
        "num_distinct_txn_per_email_7day": [round(max(i, 0)) for i in return_random_num(y, 4, 2, 2, 3, np.random.normal)],
        "ip_country_us": [round(min(i, 1)) for i in [max(i, 0) for i in return_random_num(y, 0.3, 0.4, 0.5, 0.5, np.random.normal)]],
        "email_kb_distance": [min(i, 1) for i in [max(i, 0) for i in return_random_num(y, 0.2, 0.5, 0.6, 0.4, np.random.normal)]],
        "email_alpharatio":  [min(i, 1) for i in [max(i, 0) for i in return_random_num(y, 0.33, 0.1, 0.5, 0.2, np.random.normal)]],
    },
        index=list(range(0, 1000))
    )
    columns_int = [
        'num_distinct_txn_per_email_1day', 'num_distinct_txn_per_email_7day', 'ip_country_us']
    columns_cat = ['ip_country_us']
    columns_num = ['num_distinct_txn_per_email_1day',
                   'num_distinct_txn_per_email_7day', 'email_kb_distance', 'email_alpharatio']
    weights = y.apply(lambda x: 1000 if x == 1 else 1)
    return [X, y, columns_int, columns_cat, columns_num, weights]


@pytest.fixture
def fs_instantiated():
    f = FScore(0.5)
    return f.fit


@pytest.fixture
def rg_instantiated(fs_instantiated):
    f0dot5 = fs_instantiated
    params = {
        'metric': f0dot5,
        'n_total_conditions': 4,
        'tree_ensemble': RandomForestClassifier(n_estimators=10, random_state=0),
        'precision_threshold': 0,
        'num_cores': 4
    }
    rg = RuleGeneratorDT(**params)
    rg.today = '20200204'
    return [rg, params]


@pytest.fixture
def create_dummy_rules():
    rule_descriptions = pd.DataFrame({
        'Rule': ["(X['A']>1)", "(X['A']>1)"],
        'Logic': ["(X['A']>1)", "(X['A']>1)"],
        'Precision': [0, 0],
        'Recall': [0, 0],
        'nConditions': [0, 0],
        'PercDataFlagged': [0, 0],
        'FScore': [0, 0],
        'Beta': [0, 0]
    })
    rule_descriptions.set_index('Rule', inplace=True)
    X_rules = pd.concat([pd.DataFrame({"(X['A']>1)": np.random.randint(0, 1, 100)}),
                         pd.DataFrame({"(X['A']>1)": np.random.randint(0, 1, 100)})],
                        axis=1)
    return rule_descriptions, X_rules


@ pytest.fixture
def fit_decision_tree():
    def _fit(X, y, sample_weight=None):
        dt = DecisionTreeClassifier(random_state=0, max_depth=4)
        dt.fit(X, y, sample_weight=sample_weight)
        return dt
    return _fit


def test_fit_dt(create_data, fit_decision_tree):
    X, y, _, _, _, weights = create_data
    for w in [None, weights]:
        dt = fit_decision_tree(X, y, w)
        dt_test = DecisionTreeClassifier(random_state=0, max_depth=4)
        dt_test.fit(X, y, w)
        dt_preds = dt.predict_proba(X)[:, -1]
        dt_test_preds = dt_test.predict_proba(X)[:, -1]
        assert [a == b for a, b in zip(dt_preds, dt_test_preds)]


def test_fit(create_data, rg_instantiated):

    def _assert_test_fit(rule_descriptions_shape, X_rules_shape):
        X_rules = rg.fit(X, y, sample_weight=w)
        _assert_rule_descriptions_and_X_rules(
            rg.rule_descriptions, X_rules, rule_descriptions_shape, X_rules_shape, X, y, params['metric'], w)

    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    for w in [None, weights]:
        _assert_test_fit((40, 6), (1000, 40)) if w is None else _assert_test_fit(
            (14, 6), (1000, 14))


def test_fit_target_feat_corr_types_infer(create_data, rg_instantiated):

    def _assert_test_fit(rule_descriptions_shape, X_rules_shape):
        X_rules = rg.fit(X, y, sample_weight=w)
        _assert_rule_descriptions_and_X_rules(
            rg.rule_descriptions, X_rules, rule_descriptions_shape, X_rules_shape, X, y, params['metric'], w)

    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    rg.target_feat_corr_types = 'Infer'
    for w in [None, weights]:
        _assert_test_fit((40, 6), (1000, 40)) if w is None else _assert_test_fit(
            (14, 6), (1000, 14))
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['email_alpharatio']>" in l]) == 0
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['email_kb_distance']>" in l]) == 0
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['ip_country_us']==True" in l]) == 0
        assert len([l for l in rg.rule_descriptions['Logic']
                    .values if "X['num_distinct_txn_per_email_1day']<" in l]) == 0
        assert len([l for l in rg.rule_descriptions['Logic']
                    .values if "X['num_distinct_txn_per_email_7day']<" in l]) == 0


def test_fit_target_feat_corr_types_provided(create_data, rg_instantiated):

    def _assert_test_fit(rule_descriptions_shape, X_rules_shape):
        X_rules = rg.fit(X, y, sample_weight=w)
        _assert_rule_descriptions_and_X_rules(
            rg.rule_descriptions, X_rules, rule_descriptions_shape, X_rules_shape, X, y, params['metric'], w)

    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    rg.target_feat_corr_types = {
        'PositiveCorr': [
            'num_distinct_txn_per_email_1day',
            'num_distinct_txn_per_email_7day'
        ],
        'NegativeCorr': [
            'ip_country_us', 'email_kb_distance', 'email_alpharatio']
    }
    for w in [None, weights]:
        _assert_test_fit((40, 6), (1000, 40)) if w is None else _assert_test_fit(
            (14, 6), (1000, 14))
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['email_alpharatio']>" in l]) == 0
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['email_kb_distance']>" in l]) == 0
        assert len(
            [l for l in rg.rule_descriptions['Logic'].values if "X['ip_country_us']==True" in l]) == 0
        assert len([l for l in rg.rule_descriptions['Logic']
                    .values if "X['num_distinct_txn_per_email_1day']<" in l]) == 0
        assert len([l for l in rg.rule_descriptions['Logic']
                    .values if "X['num_distinct_txn_per_email_7day']<" in l]) == 0


def test_transform(create_data, rg_instantiated):

    def _assert_test_transform(rule_descriptions_shape, X_rules_shape):
        _ = rg.fit(X, y, sample_weight=w)
        print(len(rg.rule_strings))
        X_rules_applied = rg.transform(X, y, w)
        _assert_rule_descriptions_and_X_rules(
            rg.rule_descriptions, X_rules_applied, rule_descriptions_shape, X_rules_shape, X, y, params['metric'], w)

    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    for w in [None, weights]:
        _assert_test_transform((40, 6), (1000, 40)) if w is None else _assert_test_transform(
            (14, 6), (1000, 14))


def test_extract_rules_from_ensemble(create_data, rg_instantiated):

    def _assert_extract_rules_from_ensemble(rule_descriptions_shape, X_rules_shape):
        rf = params['tree_ensemble']
        rf.fit(X, y, sample_weight=w)
        X_rules = rg._extract_rules_from_ensemble(
            X, y, rf, params['num_cores'], w, columns_int, columns_cat)
        _assert_rule_descriptions_and_X_rules(
            rg.rule_descriptions, X_rules, rule_descriptions_shape, X_rules_shape, X, y, params['metric'], w)

    X, y, columns_int, columns_cat, _, weights = create_data
    rg, params = rg_instantiated
    for w in [None, weights]:
        _assert_extract_rules_from_ensemble(
            (40, 6), (1000, 40)) if w is None else _assert_extract_rules_from_ensemble((14, 6), (1000, 14))


def test_extract_rules_from_dt(create_data, rg_instantiated, fit_decision_tree):

    expected_rule_sets_sample_weight_None = set([
        "(X['email_alpharatio']<=0.43817)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_1day']<=1)",
        "(X['email_alpharatio']<=0.43817)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_alpharatio']<=0.43844)&(X['email_alpharatio']>0.43817)&(X['email_kb_distance']>0.00092)",
        "(X['email_alpharatio']<=0.52347)&(X['email_kb_distance']<=0.00092)&(X['num_distinct_txn_per_email_1day']<=2)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_alpharatio']<=0.52347)&(X['email_kb_distance']<=0.00092)&(X['num_distinct_txn_per_email_1day']>=3)",
        "(X['email_alpharatio']>0.43844)&(X['email_kb_distance']<=0.29061)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_7day']>=5)"
    ])
    expected_rule_sets_sample_weight_given = set([
        "(X['email_alpharatio']<=0.57456)&(X['num_distinct_txn_per_email_1day']<=3)&(X['num_distinct_txn_per_email_1day']>=1)&(X['num_distinct_txn_per_email_7day']>=1)"
    ])
    X, y, columns_int, columns_cat, _, weights = create_data
    dt = fit_decision_tree(X, y, None)
    rg, _ = rg_instantiated
    rule_sets = rg._extract_rules_from_dt(
        columns=X.columns, decision_tree=dt, columns_int=columns_int, columns_cat=columns_cat)
    assert rule_sets == expected_rule_sets_sample_weight_None
    dt = fit_decision_tree(X, y, weights)
    rg, _ = rg_instantiated
    rule_sets = rg._extract_rules_from_dt(
        columns=X.columns, decision_tree=dt, columns_int=columns_int, columns_cat=columns_cat)
    assert rule_sets == expected_rule_sets_sample_weight_given
    rg, _ = rg_instantiated
    rg.precision_threshold = 1
    rule_sets = rg._extract_rules_from_dt(
        columns=X.columns, decision_tree=dt, columns_int=columns_int, columns_cat=columns_cat)
    assert rule_sets == set()


def test_train_ensemble(rg_instantiated, create_data):
    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    rg.tree_ensemble.max_depth = params['n_total_conditions']
    for w in [None, weights]:
        rg_trained = rg._train_ensemble(
            X, y, tree_ensemble=rg.tree_ensemble, sample_weight=w, verbose=0)
        rf = RandomForestClassifier(
            max_depth=params['n_total_conditions'], random_state=0, n_estimators=100)
        rf.fit(X=X, y=y, sample_weight=w)
        rf_preds = rf.predict_proba(X)[:, -1]
        rg_preds = rg_trained.predict_proba(X)[:, -1]
        assert [a == b for a, b in zip(rf_preds, rg_preds)]


def test_get_dt_attributes(create_data, rg_instantiated, fit_decision_tree):
    expected_results = (
        np.array([1,  2, -1,  4,  5, -1, -1, -1,  9, 10,
                 11, -1, -1, -1, 15, -1, 17, -1, -1]),
        np.array([8,  3, -1,  7,  6, -1, -1, -1, 14, 13,
                 12, -1, -1, -1, 16, -1, 18, -1, -1]),
        np.array([3,  0, -2,  4,  0, -2, -2, -2,  4,  4,
                 0, -2, -2, -2,  1, -2,  3, -2, -2]),
        np.array([
            0.00091782,  1.5, -2.,  0.52346626,  2.5,
            -2., -2., -2.,  0.43843633,  0.43816555,
            1.5, -2., -2., -2.,  4.5,
            -2.,  0.29061292, -2., -2.]),
        np.array([
            0.02, 0.09090909, 0., 0.21875, 0.38888889,
            0.54545455, 0.14285714, 0., 0.01408451, 0.03614458,
            0.03323263, 0.01020408, 0.06666667, 1., 0.00169205,
            0., 0.00917431, 0.06666667, 0.]),
        0.5833333333333334
    )
    X, y, _, _, _, _ = create_data
    rg, _ = rg_instantiated
    dt = fit_decision_tree(X, y, None)
    left, right, features, thresholds, node_precs, tree_prec = rg._get_dt_attributes(
        dt)
    np.testing.assert_array_almost_equal(left, expected_results[0])
    np.testing.assert_array_almost_equal(right, expected_results[1])
    np.testing.assert_array_almost_equal(features, expected_results[2])
    np.testing.assert_array_almost_equal(thresholds, expected_results[3])
    np.testing.assert_array_almost_equal(node_precs, expected_results[4])
    assert tree_prec == expected_results[5]


def test_errors(create_data, rg_instantiated):
    X, y, _, _, _, _ = create_data
    rg, _ = rg_instantiated
    with pytest.raises(TypeError, match='`X` must be a pandas.core.frame.DataFrame. Current type is list.'):
        rg.fit(X=[], y=y)
    with pytest.raises(TypeError, match='`y` must be a pandas.core.series.Series. Current type is list.'):
        rg.fit(X=X, y=[])
    with pytest.raises(TypeError, match='`sample_weight` must be a pandas.core.series.Series. Current type is list.'):
        rg.fit(X=X, y=y, sample_weight=[])

# Methods below are part of _base module ------------------------------------


def test_extract_rules_from_tree(fit_decision_tree, rg_instantiated, create_data):

    expected_rule_sets_sample_weight_None = set([
        "(X['email_alpharatio']<=0.43817)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_1day']<=1)",
        "(X['email_alpharatio']<=0.43817)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_alpharatio']<=0.43844)&(X['email_alpharatio']>0.43817)&(X['email_kb_distance']>0.00092)",
        "(X['email_alpharatio']<=0.52347)&(X['email_kb_distance']<=0.00092)&(X['num_distinct_txn_per_email_1day']<=2)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_alpharatio']<=0.52347)&(X['email_kb_distance']<=0.00092)&(X['num_distinct_txn_per_email_1day']>=3)",
        "(X['email_alpharatio']>0.43844)&(X['email_kb_distance']<=0.29061)&(X['email_kb_distance']>0.00092)&(X['num_distinct_txn_per_email_7day']>=5)"
    ])

    expected_rule_sets_sample_weight_given = set([
        "(X['email_alpharatio']<=0.57456)&(X['num_distinct_txn_per_email_1day']<=3)&(X['num_distinct_txn_per_email_1day']>=1)&(X['num_distinct_txn_per_email_7day']>=1)"
    ])
    X, y, columns_int, columns_cat, _, weights = create_data
    dt = fit_decision_tree(X, y, None)
    rg, _ = rg_instantiated
    left, right, features, thresholds, precisions, _ = rg._get_dt_attributes(
        dt)
    rule_sets = rg._extract_rules_from_tree(
        columns=X.columns.tolist(), precision_threshold=rg.precision_threshold,
        columns_int=columns_int, columns_cat=columns_cat, left=left,
        right=right, features=features, thresholds=thresholds,
        precisions=precisions
    )
    assert rule_sets == expected_rule_sets_sample_weight_None
    dt = fit_decision_tree(X, y, weights)
    rg, _ = rg_instantiated
    left, right, features, thresholds, precisions, _ = rg._get_dt_attributes(
        dt)
    rule_sets = rg._extract_rules_from_tree(
        columns=X.columns.tolist(), precision_threshold=rg.precision_threshold,
        columns_int=columns_int, columns_cat=columns_cat, left=left,
        right=right, features=features, thresholds=thresholds,
        precisions=precisions
    )
    assert rule_sets == expected_rule_sets_sample_weight_given
    rg, _ = rg_instantiated
    rg.precision_threshold = 1
    left, right, features, thresholds, precisions, _ = rg._get_dt_attributes(
        dt)
    rule_sets = rg._extract_rules_from_tree(
        columns=X.columns.tolist(), precision_threshold=rg.precision_threshold,
        columns_int=columns_int, columns_cat=columns_cat, left=left,
        right=right, features=features, thresholds=thresholds,
        precisions=precisions
    )
    assert rule_sets == set()


def test_calc_target_ratio_wrt_features(rg_instantiated):
    X = pd.DataFrame({
        'A': [10, 9, 8, 7, 6, 5],
        'B': [10, 10, 0, 0, 0, 0],
        'C': [0, 1, 2, 3, 4, 5],
        'D': [0, 0, 10, 10, 10, 10]
    })
    y = pd.Series([1, 1, 1, 0, 0, 0])
    expected_result = {
        'PositiveCorr': ['A', 'B'],
        'NegativeCorr': ['C', 'D'],
    }
    rg, _ = rg_instantiated
    target_feat_corr_types = rg._calc_target_ratio_wrt_features(X, y)
    assert target_feat_corr_types == expected_result

# Methods for comparing results to expected ----------------------------------


def _calc_rule_metrics(rule, X, y, metric, sample_weight):
    X_rule = eval(rule).astype(int)
    prec = precision_score(
        y, X_rule, sample_weight=sample_weight, zero_division=0)
    rec = recall_score(y, X_rule, sample_weight=sample_weight,
                       zero_division=0)
    opt_value = metric(X_rule, y, sample_weight=sample_weight)
    perc_data_flagged = X_rule.mean()
    return [prec, rec, perc_data_flagged, opt_value, X_rule]


def _assert_rule_descriptions(rule_descriptions, X, y, metric, sample_weight):
    for _, row in rule_descriptions.iterrows():
        class_results = row.loc[['Precision', 'Recall',
                                'PercDataFlagged', 'Metric']].values.astype(float)
        rule = row['Logic']
        test_results = _calc_rule_metrics(rule, X, y, metric, sample_weight)
        for i in range(0, len(class_results)):
            assert round(class_results[i], 6) == round(test_results[i], 6)


def _assert_X_rules(X_rules, rule_list, X, y, metric, sample_weight):
    for rule, rule_name in zip(rule_list, X_rules):
        class_result = X_rules[rule_name]
        test_result = _calc_rule_metrics(
            rule, X, y, metric, sample_weight)[-1]
        assert [a == b for a, b in zip(class_result, test_result)]


def _assert_rule_descriptions_and_X_rules(rule_descriptions, X_rules, rule_descriptions_shape,
                                          X_rules_shape, X, y, metric, sample_weight):
    assert rule_descriptions.shape == rule_descriptions_shape
    assert X_rules.shape == X_rules_shape
    _assert_rule_descriptions(rule_descriptions, X, y, metric, sample_weight)
    _assert_X_rules(
        X_rules, rule_descriptions['Logic'].values, X, y, metric, sample_weight)
