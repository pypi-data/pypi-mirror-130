import pytest
import numpy as np
import pandas as pd
import databricks.koalas as ks
from iguanas.rule_generation import RuleGeneratorDTSpark
from iguanas.metrics.classification import FScore
from pyspark.ml.classification import RandomForestClassifier as RandomForestClassifierSpark
from pyspark.ml.feature import VectorAssembler
import random
from sklearn.metrics import precision_score, recall_score, fbeta_score


@pytest.fixture
def create_data():
    def return_random_num(y, fraud_min, fraud_max, nonfraud_min, nonfraud_max, rand_func):
        data = [rand_func(fraud_min, fraud_max) if i == 1 else rand_func(
            nonfraud_min, nonfraud_max) for i in y]
        return data

    random.seed(0)
    np.random.seed(0)
    y = pd.Series(data=[0]*95 + [1]*5, index=list(range(0, 100)))
    X = ks.DataFrame(data={
        "num_distinct_txn_per_email_1day": [round(max(i, 0)) for i in return_random_num(y, 2, 1, 1, 2, np.random.normal)],
        "num_distinct_txn_per_email_7day": [round(max(i, 0)) for i in return_random_num(y, 4, 2, 2, 3, np.random.normal)],
        "ip_country_us": [round(min(i, 1)) for i in [max(i, 0) for i in return_random_num(y, 0.3, 0.4, 0.5, 0.5, np.random.normal)]],
        "email_kb_distance": [min(i, 1) for i in [max(i, 0) for i in return_random_num(y, 0.2, 0.5, 0.6, 0.4, np.random.normal)]],
        "email_alpharatio":  [min(i, 1) for i in [max(i, 0) for i in return_random_num(y, 0.33, 0.1, 0.5, 0.2, np.random.normal)]],
    },
        index=list(range(0, 100))
    )
    columns_int = [
        'num_distinct_txn_per_email_1day', 'num_distinct_txn_per_email_7day', 'ip_country_us']
    columns_cat = ['ip_country_us']
    columns_num = ['num_distinct_txn_per_email_1day',
                   'num_distinct_txn_per_email_7day', 'email_kb_distance', 'email_alpharatio']
    weights = ks.Series(y.apply(lambda x: 100 if x == 1 else 1))
    y = ks.from_pandas(y)
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
        'tree_ensemble': RandomForestClassifierSpark(bootstrap=False, numTrees=1, impurity='gini')
    }
    rgs = RuleGeneratorDTSpark(**params)
    rgs.today = '20200204'
    return rgs, params


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
    X_rules = ks.DataFrame([
        np.random.randint(0, 1, 100),
        np.random.randint(0, 1, 100)
    ], columns=["(X['A']>1)", "(X['A']>1)"])
    return rule_descriptions, X_rules


@pytest.fixture
def create_spark_df(create_data):
    X, y, _, _, _, weights = create_data
    spark_df = X.join(y.rename('label_')).to_spark()
    spark_df_weights = X.join(y.rename('label_')).join(
        weights.rename('sample_weight_')).to_spark()
    vectorAssembler = VectorAssembler(
        inputCols=X.columns.tolist(), outputCol="features")
    spark_df = vectorAssembler.transform(spark_df)
    spark_df_weights = vectorAssembler.transform(spark_df_weights)
    return spark_df, spark_df_weights


@pytest.fixture
def train_rf(create_spark_df):
    spark_df, _ = create_spark_df
    rf = RandomForestClassifierSpark(
        bootstrap=False, numTrees=1, seed=0, labelCol='label_',
        featuresCol='features', impurity='gini'
    )
    trained_rf = rf.fit(spark_df)
    return trained_rf


def test_fit(create_data, rg_instantiated):

    expected_rule_descriptions_wo_weights = np.array(
        [
            [1.0, 0.6, 0.03, 0.8823529411764707,
             "(X['email_alpharatio']<=0.29912)&(X['email_alpharatio']>0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
             3],
            [0.4, 0.4, 0.05, 0.4000000000000001,
             "(X['email_alpharatio']<=0.33992)&(X['email_alpharatio']>0.29912)&(X['num_distinct_txn_per_email_7day']>=4)",
             3]
        ], dtype=object)
    expected_rule_descriptions_weights = np.array(
        [
            [0.998003992015968, 1.0, 0.06, 0.9984025559105432,
             "(X['email_alpharatio']<=0.32306)&(X['email_alpharatio']>0.22241)&(X['num_distinct_txn_per_email_1day']>=1)&(X['num_distinct_txn_per_email_7day']>=4)",
             4]
        ], dtype=object)
    X, y, _, _, _, weights = create_data
    rg, params = rg_instantiated
    X_rules = rg.fit(X, y, None)
    _assert_rule_descriptions_and_X_rules(
        rg.rule_descriptions, X_rules, (2, 6), (100, 2), X, y, params['metric'], None)
    np.testing.assert_array_equal(
        rg.rule_descriptions.values, expected_rule_descriptions_wo_weights)
    assert rg.rule_descriptions['nConditions'].max() <= 4
    X_rules = rg.fit(X, y, weights)
    _assert_rule_descriptions_and_X_rules(
        rg.rule_descriptions, X_rules, (1, 6), (100, 1), X, y, params['metric'], weights)
    np.testing.assert_array_equal(
        rg.rule_descriptions.values, expected_rule_descriptions_weights)
    assert rg.rule_descriptions['nConditions'].max() <= 4


def test_fit_target_feat_corr_types_infer(create_data, rg_instantiated):

    expected_rule_descriptions = np.array(
        [
            [0.38461538461538464, 1.0, 0.13, 0.43859649122807015,
             "(X['email_alpharatio']<=0.33992)&(X['num_distinct_txn_per_email_7day']>=4)",
             2],
            [0.375, 0.6, 0.08, 0.4054054054054054,
             "(X['email_alpharatio']<=0.29912)&(X['num_distinct_txn_per_email_7day']>=4)",
             2],
            [0.2, 1.0, 0.25, 0.23809523809523808,
             "(X['email_alpharatio']<=0.33992)", 1],
            [0.0, 0.0, 0.05, 0.0,
             "(X['email_alpharatio']<=0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
             2]
        ], dtype=object)
    X, y, _, _, _, _ = create_data
    rg, params = rg_instantiated
    rg.precision_threshold = -1
    rg.target_feat_corr_types = 'Infer'
    X_rules = rg.fit(X, y, None)
    _assert_rule_descriptions_and_X_rules(
        rg.rule_descriptions, X_rules, (4, 6), (100, 4), X, y, params['metric'], None)
    np.testing.assert_array_equal(
        rg.rule_descriptions.values, expected_rule_descriptions)


def test_extract_rules_from_ensemble(create_data, create_spark_df, train_rf, rg_instantiated):
    expected_rule_descriptions = np.array([
        [0.0, 0.0, 0.05, 0.0,
         "(X['email_alpharatio']<=0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
         2],
        [1.0, 0.6, 0.03, 0.8823529411764707,
            "(X['email_alpharatio']<=0.29912)&(X['email_alpharatio']>0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
            3],
        [0.0, 0.0, 0.02, 0.0,
            "(X['email_alpharatio']<=0.30749)&(X['email_alpharatio']>0.29912)&(X['num_distinct_txn_per_email_7day']>=4)",
            3],
        [0.6666666666666666, 0.4, 0.03, 0.5882352941176471,
            "(X['email_alpharatio']<=0.33992)&(X['email_alpharatio']>0.30749)&(X['num_distinct_txn_per_email_7day']>=4)",
            3],
        [0.0, 0.0, 0.12, 0.0,
            "(X['email_alpharatio']<=0.33992)&(X['num_distinct_txn_per_email_7day']<=3)",
            2],
        [0.0, 0.0, 0.75, 0.0, "(X['email_alpharatio']>0.33992)", 1]],
        dtype=object)
    X, y, columns_int, columns_cat, _, _ = create_data
    spark_df, _ = create_spark_df
    rf_trained = train_rf
    rg, _ = rg_instantiated
    rg.precision_threshold = -1
    X_rules = rg._extract_rules_from_ensemble(
        X, y, None, rf_trained, columns_int, columns_cat)
    assert X_rules.shape == (100, 6)
    assert all(np.sort(X_rules.sum().to_numpy())
               == np.array([2, 3, 3, 5, 12, 75]))
    rg.rule_descriptions.sort_values('Logic', inplace=True)
    np.testing.assert_array_equal(
        rg.rule_descriptions.values, expected_rule_descriptions)


def test_extract_rules_from_dt(create_data, train_rf, rg_instantiated):
    expected_results = {
        "(X['email_alpharatio']<=0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
        "(X['email_alpharatio']<=0.29912)&(X['email_alpharatio']>0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
        "(X['email_alpharatio']<=0.30749)&(X['email_alpharatio']>0.29912)&(X['num_distinct_txn_per_email_7day']>=4)",
        "(X['email_alpharatio']<=0.33992)&(X['email_alpharatio']>0.30749)&(X['num_distinct_txn_per_email_7day']>=4)",
        "(X['email_alpharatio']<=0.33992)&(X['num_distinct_txn_per_email_7day']<=3)",
        "(X['email_alpharatio']>0.33992)"
    }
    X, _, columns_int, columns_cat, _, _ = create_data
    rf_trained = train_rf
    rg, _ = rg_instantiated
    rg.precision_threshold = -1
    rule_strings = rg._extract_rules_from_dt(
        X.columns.tolist(), rf_trained.trees[0], columns_int, columns_cat)
    assert rule_strings == expected_results


def test_create_train_spark_df(create_data, create_spark_df, rg_instantiated):
    X, y, _, _, _, weights = create_data
    expected_spark_df, expected_spark_df_weights = create_spark_df
    rg, _ = rg_instantiated
    spark_df = rg._create_train_spark_df(X=X, y=y, sample_weight=None)
    assert spark_df.columns == expected_spark_df.columns
    spark_df_weights = rg._create_train_spark_df(
        X=X, y=y, sample_weight=weights)
    assert spark_df_weights.columns == expected_spark_df_weights.columns
    assert spark_df.count() == spark_df_weights.count() == 100


def test_get_pyspark_tree_structure(train_rf, rg_instantiated):
    expected_left_children, expected_right_children, expected_features, expected_thresholds, expected_precisions = (
        np.array([1,  2, -1,  4, -1,  6, -1,  8, -1, -1, -1]),
        np.array([10,  3, -1,  5, -1,  7, -1,  9, -1, -1, -1]),
        np.array([4,  1, -2,  4, -2,  4, -2,  4, -2, -2, -2]),
        np.array([0.33992341, 3.5, -2.,  0.22240729, -2.,
                  0.29912349, -2., 0.30748836, -2., -2., -2.]),
        np.array([0.05, 0.2, 0., 0.38461538, 0., 0.625, 1.,
                  0.4, 0., 0.66666667, 0.])
    )
    rf_trained = train_rf
    rg, _ = rg_instantiated
    left_children, right_children, features, thresholds, precisions, tree_prec = rg._get_pyspark_tree_structure(
        rf_trained.trees[0]._call_java('rootNode'))
    assert all(left_children == expected_left_children)
    assert all(right_children == expected_right_children)
    assert all(features == expected_features)
    np.testing.assert_array_almost_equal(thresholds, expected_thresholds)
    np.testing.assert_array_almost_equal(precisions, expected_precisions)
    assert tree_prec == 0.8333333333333334


def test_transform(create_data, rg_instantiated):
    expected_rule_descriptions = np.array([
        [0.11363636363636363, 1.0, 0.44, 0.13812154696132597,
         "(X['num_distinct_txn_per_email_1day']>1)", 1]], dtype=object)
    X, y, _, _, _, _ = create_data
    rg, _ = rg_instantiated
    rg.rule_strings = {'Rule1': "(X['num_distinct_txn_per_email_1day']>1)"}
    X_rules = rg.transform(X, y)
    assert X_rules.sum()[0] == 44
    np.testing.assert_array_equal(
        rg.rule_descriptions, expected_rule_descriptions)


def test_errors(create_data, rg_instantiated):
    X, y, _, _, _, _ = create_data
    rg, _ = rg_instantiated
    with pytest.raises(TypeError, match='`X` must be a databricks.koalas.frame.DataFrame. Current type is list.'):
        rg.fit(X=[], y=y)
    with pytest.raises(TypeError, match='`y` must be a databricks.koalas.series.Series. Current type is list.'):
        rg.fit(X=X, y=[])
    with pytest.raises(TypeError, match='`sample_weight` must be a databricks.koalas.series.Series. Current type is list.'):
        rg.fit(X=X, y=y, sample_weight=[])


# Methods below are part of _base module ------------------------------------


def test_extract_rules_from_tree(train_rf, rg_instantiated, create_data):

    expected_rule_sets = set([
        "(X['email_alpharatio']<=0.29912)&(X['email_alpharatio']>0.22241)&(X['num_distinct_txn_per_email_7day']>=4)",
        "(X['email_alpharatio']<=0.33992)&(X['email_alpharatio']>0.30749)&(X['num_distinct_txn_per_email_7day']>=4)"
    ])
    X, _, columns_int, columns_cat, _, _ = create_data
    rg, _ = rg_instantiated
    rf_trained = train_rf
    left, right, features, thresholds, precisions, _ = rg._get_pyspark_tree_structure(
        rf_trained.trees[0]._call_java('rootNode'))
    rule_sets = rg._extract_rules_from_tree(
        columns=X.columns.tolist(), precision_threshold=rg.precision_threshold,
        columns_int=columns_int, columns_cat=columns_cat, left=left,
        right=right, features=features, thresholds=thresholds,
        precisions=precisions
    )
    assert rule_sets == expected_rule_sets
    rg, _ = rg_instantiated
    rg.precision_threshold = 1
    left, right, features, thresholds, precisions, _ = rg._get_pyspark_tree_structure(
        rf_trained.trees[0]._call_java('rootNode'))
    rule_sets = rg._extract_rules_from_tree(
        columns=X.columns.tolist(), precision_threshold=rg.precision_threshold,
        columns_int=columns_int, columns_cat=columns_cat, left=left,
        right=right, features=features, thresholds=thresholds,
        precisions=precisions
    )
    assert rule_sets == set()


def test_calc_target_ratio_wrt_features(rg_instantiated):
    X = ks.DataFrame({
        'A': [10, 9, 8, 7, 6, 5],
        'B': [10, 10, 0, 0, 0, 0],
        'C': [0, 1, 2, 3, 4, 5],
        'D': [0, 0, 10, 10, 10, 10]
    })
    y = ks.Series([1, 1, 1, 0, 0, 0])
    expected_result = {
        'PositiveCorr': ['A', 'B'],
        'NegativeCorr': ['C', 'D'],
    }
    rg, _ = rg_instantiated
    target_feat_corr_types = rg._calc_target_ratio_wrt_features(X, y)
    assert target_feat_corr_types == expected_result

# Methods for comparing results to expected ----------------------------------


def _calc_rule_metrics(rule, X, y, sample_weight):
    X_rule = eval(rule).astype(int)
    if sample_weight is not None:
        sample_weight = sample_weight.to_pandas()
    prec = precision_score(
        y.to_pandas(), X_rule.to_pandas(), sample_weight=sample_weight)
    rec = recall_score(y.to_pandas(), X_rule.to_pandas(),
                       sample_weight=sample_weight)
    opt_value = fbeta_score(y.to_pandas(), X_rule.to_pandas(),
                            sample_weight=sample_weight, beta=0.5)
    perc_data_flagged = X_rule.mean()
    return [prec, rec, perc_data_flagged, opt_value, X_rule]


def _assert_rule_descriptions(rule_descriptions, X, y, metric, sample_weight):
    for _, row in rule_descriptions.iterrows():
        class_results = row.loc[['Precision', 'Recall',
                                'PercDataFlagged', 'Metric']].values.astype(float)
        rule = row['Logic']
        test_results = _calc_rule_metrics(rule, X, y, sample_weight)
        for i in range(0, len(class_results)):
            assert round(class_results[i], 6) == round(test_results[i], 6)


def _assert_X_rules(X_rules, rule_list, X, y, metric, sample_weight):
    for rule, rule_name in zip(rule_list, X_rules):
        class_result = X_rules[rule_name]
        test_result = _calc_rule_metrics(
            rule, X, y, sample_weight)[-1]
        assert [a == b for a, b in zip(
            class_result.to_numpy(), test_result.to_numpy())]


def _assert_rule_descriptions_and_X_rules(rule_descriptions, X_rules, rule_descriptions_shape,
                                          X_rules_shape, X, y, metric, sample_weight):
    assert rule_descriptions.shape == rule_descriptions_shape
    assert X_rules.shape == X_rules_shape
    _assert_rule_descriptions(rule_descriptions, X, y, metric, sample_weight)
    _assert_X_rules(
        X_rules, rule_descriptions['Logic'].values, X, y, metric, sample_weight)
