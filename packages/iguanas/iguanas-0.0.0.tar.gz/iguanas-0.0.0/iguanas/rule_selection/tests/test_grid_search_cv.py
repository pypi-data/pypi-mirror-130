import pytest
import numpy as np
import pandas as pd
from iguanas.rule_selection import GridSearchCV, GreedyFilter
from iguanas.rule_generation import RuleGeneratorDT
from iguanas.metrics.classification import FScore, Precision
from iguanas.rule_optimisation import BayesianOptimiser
from hyperopt import tpe, anneal
from iguanas.rules import Rules
from sklearn.ensemble import RandomForestClassifier
import random
from numpy.testing import assert_array_equal


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
    weights = y.apply(lambda x: 1000 if x == 1 else 1)
    return [X, y, weights]


@pytest.fixture
def instantiate_fscore():
    fs = FScore(beta=0.5)
    return fs


# @pytest.fixture
# def instantiate_fscore():
#     fs = FScore(beta=0.5)
#     return fs


@pytest.fixture
def param_grid(instantiate_fscore):
    fs = instantiate_fscore
    param_grid = {
        'metric': [fs.fit],
        'n_total_conditions': [3, 4],
        'tree_ensemble': [
            RandomForestClassifier(n_estimators=10, random_state=0),
            RandomForestClassifier(n_estimators=50, random_state=0),
        ],
        'precision_threshold': [0],
        'num_cores': [1],
        'target_feat_corr_types': ['Infer']
    }
    return param_grid


# @pytest.fixture
# def rules_for_opt():
#     rule_strings = {
#         'Rule1': "(X['num_distinct_txn_per_email_1day']>=1)",
#         'Rule2': "(X['email_kb_distance']<=1)",
#         'Rule3': "(X['email_alpharatio']<=1)",
#         'Rule4': "(X['num_distinct_txn_per_email_7day']>=1)",
#     }
#     rules = Rules(rule_strings=rule_strings)
#     _ = rules.as_rule_lambdas(
#         as_numpy=False, with_kwargs=True
#     )
#     return rules


# @pytest.fixture
# def suggest_algos():
#     return tpe.suggest, anneal.suggest


# @pytest.fixture
# def param_grid_ro(rules_for_opt, instantiate_fscore, suggest_algos):
#     fs = instantiate_fscore
#     tpe_suggest, anneal_suggest = suggest_algos
#     f4 = FScore(beta=4)
#     rules = rules_for_opt
#     param_grid = {
#         'rule_lambdas': [rules.rule_lambdas],
#         'lambda_kwargs': [rules.lambda_kwargs],
#         'metric': [fs.fit, f4.fit],
#         'n_iter': [10],
#         'algorithm': [tpe_suggest, anneal_suggest],
#         'verbose': [0]
#     }
#     return param_grid


@pytest.fixture
def instantiate_gs_cv(instantiate_fscore, param_grid):
    fs = instantiate_fscore
    p = Precision()
    param_grid = param_grid
    rg = RuleGeneratorDT
    rg.today = '20210506'
    gs = GridSearchCV(
        rule_class=rg,
        param_grid=param_grid,
        scorer=GreedyFilter(metric=fs.fit, sorting_metric=p.fit),
        num_cores=2,
        cv=3,
        verbose=1
    )
    return gs


@pytest.fixture
# def instantiate_gs_cv_ro(instantiate_fscore, param_grid_ro):
def instantiate_gs_cv_ro():
    # fs = instantiate_fscore
    # p = Precision()
    # param_grid = param_grid_ro
    # ro = BayesianOptimiser
    # gs = GridSearchCV(
    #     rule_class=ro,
    #     param_grid=param_grid,
    #     scorer=GreedyFilter(metric=fs.fit, sorting_metric=p.fit),
    #     cv=3,
    #     num_cores=2,
    #     verbose=1
    # )
    fs = FScore(beta=0.5)
    p = Precision()
    tpe_suggest, anneal_suggest = tpe.suggest, anneal.suggest
    f4 = FScore(beta=4)
    rule_strings = {
        'Rule1': "(X['num_distinct_txn_per_email_1day']>=1)",
        'Rule2': "(X['email_kb_distance']<=1)",
        'Rule3': "(X['email_alpharatio']<=1)",
        'Rule4': "(X['num_distinct_txn_per_email_7day']>=1)",
    }
    rules = Rules(rule_strings=rule_strings)
    _ = rules.as_rule_lambdas(
        as_numpy=False, with_kwargs=True
    )
    param_grid = {
        'rule_lambdas': [rules.rule_lambdas],
        'lambda_kwargs': [rules.lambda_kwargs],
        'metric': [fs.fit, f4.fit],
        'n_iter': [10],
        'algorithm': [tpe_suggest, anneal_suggest],
        'verbose': [0]
    }
    ro = BayesianOptimiser
    gs = GridSearchCV(
        rule_class=ro,
        param_grid=param_grid,
        scorer=GreedyFilter(metric=fs.fit, sorting_metric=p.fit),
        cv=3,
        num_cores=2,
        verbose=1
    )
    return gs, fs, tpe_suggest, anneal_suggest


@pytest.fixture
def params(instantiate_fscore):
    fs = instantiate_fscore
    params = {
        'metric': fs.fit,
        'n_total_conditions': 4,
        'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
        'precision_threshold': 0,
        'num_cores': 1,
        'target_feat_corr_types': 'Infer'
    }
    return params


def test_fit_rule_gen(create_data, instantiate_gs_cv, instantiate_fscore):
    fs = instantiate_fscore
    expected_best_params = {
        'metric': fs.fit,
        'n_total_conditions': 4,
        'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
        'precision_threshold': 0,
        'num_cores': 1,
        'target_feat_corr_types': 'Infer'
    }
    expected_mean_perf = np.array(
        [0.23161798, 0.292237, 0.3315058, 0.44476211]
    )
    expected_std_perf = np.array(
        [0.11396842, 0.04597797, 0.09702325, 0.10407437]
    )
    expected_best_rule_strings = [
        "(X['email_alpharatio']<=0.37273)&(X['email_kb_distance']<=0.00655)&(X['ip_country_us']==False)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_alpharatio']<=0.30384)&(X['email_kb_distance']<=0.24568)&(X['ip_country_us']==False)&(X['num_distinct_txn_per_email_7day']>=6)"
    ]
    X, y, _ = create_data
    gs = instantiate_gs_cv
    gs.fit(X=X, y=y)
    for param_name, param_value in gs.best_params.items():
        if param_name == 'tree_ensemble':
            assert param_value.n_estimators == expected_best_params['tree_ensemble'].n_estimators
        else:
            assert param_value == expected_best_params[param_name]
    assert all(np.isclose(gs.param_results_aggregated[
        'MeanPerformance'].values, expected_mean_perf))
    assert all(np.isclose(gs.param_results_aggregated[
        'StdDevPerformance'].values, expected_std_perf))
    assert gs.best_score == 0.4447621102600064
    assert all([a == b for a, b in zip(
        gs.rule_strings.values(), expected_best_rule_strings)])
    # Check that with refilter=False, rules aren't filtered
    gs = instantiate_gs_cv
    gs.refilter = False
    gs.fit(X=X, y=y)
    assert len(gs.rule_strings) == 198


def test_fit_rule_gen_sample_weight(create_data, instantiate_gs_cv, instantiate_fscore):
    fs = instantiate_fscore
    expected_best_params = {
        'metric': fs.fit,
        'n_total_conditions': 3,
        'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
        'precision_threshold': 0,
        'num_cores': 1,
        'target_feat_corr_types': 'Infer'
    }
    expected_mean_perf = np.array(
        [0.98875845, 0.98971138, 0.98818784, 0.98764088]
    )
    expected_std_perf = np.array(
        [0.00141288, 0.00207128, 0.00145541, 0.00356849]
    )
    expected_best_rule_strings = [
        "(X['email_alpharatio']<=0.43844)&(X['num_distinct_txn_per_email_1day']>=1)&(X['num_distinct_txn_per_email_7day']>=1)",
        "(X['email_kb_distance']<=0.28886)&(X['num_distinct_txn_per_email_1day']>=2)",
        "(X['email_kb_distance']<=0.23452)&(X['ip_country_us']==False)&(X['num_distinct_txn_per_email_7day']>=1)"
    ]
    X, y, weights = create_data
    gs = instantiate_gs_cv
    gs.fit(X=X, y=y, sample_weight=weights)
    for param_name, param_value in gs.best_params.items():
        if param_name == 'tree_ensemble':
            assert param_value.n_estimators == expected_best_params['tree_ensemble'].n_estimators
        else:
            assert param_value == expected_best_params[param_name]
    assert all(np.isclose(gs.param_results_aggregated[
        'MeanPerformance'].values, expected_mean_perf))
    assert all(np.isclose(gs.param_results_aggregated[
        'StdDevPerformance'].values, expected_std_perf))
    assert gs.best_score == 0.9897113793277743
    assert all([a == b for a, b in zip(
        gs.rule_strings.values(), expected_best_rule_strings)])
    # Check that with refilter=False, rules aren't filtered
    gs = instantiate_gs_cv
    gs.refilter = False
    gs.fit(X=X, y=y, sample_weight=weights)
    assert len(gs.rule_strings) == 45


# def test_fit_rule_opt(create_data, instantiate_gs_cv_ro, instantiate_fscore,
#                       suggest_algos):
def test_fit_rule_opt(create_data, instantiate_gs_cv_ro):
    # _, anneal_suggest = suggest_algos
    # fs = instantiate_fscore
    gs, fs, _, anneal_suggest = instantiate_gs_cv_ro
    expected_best_params = {
        'metric': fs.fit,
        'algorithm': anneal_suggest
    }
    expected_mean_perf = np.array(
        [0.07209124, 0.07637765, 0.06302572, 0.06213225]
    )
    expected_std_perf = np.array(
        [0.02175542, 0.02070828, 0.01200294, 0.01073942]
    )
    expected_best_rule_strings = [
        "(X['email_kb_distance']<=0.08910864420257193)"
    ]
    X, y, _ = create_data
    # gs = instantiate_gs_cv_ro
    gs.fit(X=X, y=y)
    for param_name, param_value in gs.best_params.items():
        if param_name not in expected_best_params.keys():
            continue
        else:
            assert param_value == expected_best_params[param_name]
    assert all(np.isclose(gs.param_results_aggregated[
        'MeanPerformance'].values, expected_mean_perf))
    assert all(np.isclose(gs.param_results_aggregated[
        'StdDevPerformance'].values, expected_std_perf))
    assert gs.best_score == 0.0763776483946561
    assert all([a == b for a, b in zip(
        gs.rule_strings.values(), expected_best_rule_strings)])


def test_fit_rule_opt_refilter(create_data, instantiate_gs_cv_ro):
    # Need to re-instantiate grid search class, otherwise get pickling
    # errors when running in parallel
    X, y, _ = create_data
    gs, _, _, _ = instantiate_gs_cv_ro
    gs.refilter = False
    gs.fit(X=X, y=y)
    assert len(gs.rule_strings) == 4


def test_fit_rule_opt_sample_weight(create_data, instantiate_gs_cv_ro):
    # fs = instantiate_fscore
    # tpe_suggest, _ = suggest_algos
    gs, fs, tpe_suggest, _ = instantiate_gs_cv_ro
    expected_best_params = {
        'metric': fs.fit,
        'algorithm': tpe_suggest
    }
    expected_mean_perf = np.array(
        [0.97786715, 0.97786715, 0.97786715, 0.97786715]
    )
    expected_std_perf = np.array(
        [0.00102126, 0.00102126, 0.00102126, 0.00102126]
    )
    expected_best_rule_strings = [
        "(X['num_distinct_txn_per_email_1day']>=1.0)"
    ]
    X, y, weights = create_data
    # gs, _, _, _ = instantiate_gs_cv_ro
    gs.fit(X=X, y=y, sample_weight=weights)
    for param_name, param_value in gs.best_params.items():
        if param_name not in expected_best_params.keys():
            continue
        else:
            assert param_value == expected_best_params[param_name]
    assert all(np.isclose(gs.param_results_aggregated[
        'MeanPerformance'].values, expected_mean_perf))
    assert all(np.isclose(gs.param_results_aggregated[
        'StdDevPerformance'].values, expected_std_perf))
    assert gs.best_score == 0.9778671462188098
    assert all([a == b for a, b in zip(
        gs.rule_strings.values(), expected_best_rule_strings)])
    # # Check that with refilter=False, rules aren't filtered
    # gs = instantiate_gs_cv_ro
    # gs.refilter = False
    # gs.fit(X=X, y=y, sample_weight=weights)
    # assert len(gs.rule_strings) == 4


def test_fit_rule_opt_sample_weight_refilter(create_data, instantiate_gs_cv_ro):
    # Need to re-instantiate grid search class, otherwise get pickling
    # errors when running in parallel
    X, y, weights = create_data
    gs, _, _, _ = instantiate_gs_cv_ro
    gs.refilter = False
    gs.fit(X=X, y=y, sample_weight=weights)
    assert len(gs.rule_strings) == 4


def test_transform(create_data, instantiate_gs_cv):
    expected_rule_descriptions_values = np.array(
        [[0.6666666666666666, 0.2, 0.006, 0.4545454545454545,
          "(X['email_alpharatio']<=0.37273)&(X['email_kb_distance']<=0.00655)&(X['ip_country_us']==False)&(X['num_distinct_txn_per_email_1day']>=2)",
          4],
         [1.0, 0.1, 0.002, 0.3571428571428572,
          "(X['email_alpharatio']<=0.30384)&(X['email_kb_distance']<=0.24568)&(X['ip_country_us']==False)&(X['num_distinct_txn_per_email_7day']>=6)",
          4]], dtype=object)
    X, y, _ = create_data
    gs = instantiate_gs_cv
    gs.fit(X=X, y=y)
    X_rules = gs.transform(X=X, y=y)
    assert X_rules.mean().mean() == 0.004
    assert_array_equal(
        gs.rule_descriptions.values, expected_rule_descriptions_values)


def test_fit_on_fold_with_params(instantiate_gs_cv_ro, create_data):
    gs, _, _, _ = instantiate_gs_cv_ro
    X, y, _ = create_data
    params_perf = gs._fit_on_fold_with_params(
        gs.param_combinations[0], X=X, y=y, sample_weight=None,
        train_idxs=list(range(0, 600)) + list(range(990, 1000)),
        val_idxs=list(range(600, 990)), fold_idx=0, param_set_idx=0
    )
    assert params_perf == 0.08064516129032258


def test_set_up_dataset(create_data, instantiate_gs_cv):
    X, y, weights = create_data
    train_idxs = list(range(0, 600)) + list(range(990, 1000))
    val_idxs = list(range(600, 990))
    gs = instantiate_gs_cv
    X_train, y_train, sample_weight_train, X_val, y_val, sample_weight_val = gs._set_up_datasets(
        X=X, y=y, sample_weight=None, train_idxs=train_idxs, val_idxs=val_idxs)
    assert all(X_train.index == train_idxs)
    assert all(y_train.index == train_idxs)
    assert sample_weight_train is None
    assert all(X_val.index == val_idxs)
    assert all(y_val.index == val_idxs)
    assert sample_weight_val is None
    X_train, y_train, sample_weight_train, X_val, y_val, sample_weight_val = gs._set_up_datasets(
        X=X, y=y, sample_weight=weights, train_idxs=train_idxs, val_idxs=val_idxs)
    assert all(X_train.index == train_idxs)
    assert all(y_train.index == train_idxs)
    assert all(sample_weight_train.index == train_idxs)
    assert all(X_val.index == val_idxs)
    assert all(y_val.index == val_idxs)
    assert all(sample_weight_val.index == val_idxs)


def test_calculate_aggregated_perf(instantiate_fscore, instantiate_gs_cv):
    fs = instantiate_fscore
    gs = instantiate_gs_cv
    param_combinations = {
        0: {
            'metric': fs.fit,
            'n_total_conditions': 3,
            'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
            'precision_threshold': 0,
            'num_cores': 1,
            'target_feat_corr_types': 'Infer'},
        1: {
            'metric': fs.fit,
            'n_total_conditions': 3,
            'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
            'precision_threshold': 0,
            'num_cores': 1,
            'target_feat_corr_types': 'Infer'},
        2: {
            'metric': fs.fit,
            'n_total_conditions': 4,
            'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
            'precision_threshold': 0,
            'num_cores': 1,
            'target_feat_corr_types': 'Infer'},
        3: {
            'metric': fs.fit,
            'n_total_conditions': 4,
            'tree_ensemble': RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
            'precision_threshold': 0,
            'num_cores': 1,
            'target_feat_corr_types': 'Infer'}
    }
    param_results_per_fold = pd.DataFrame({
        'Fold': {0: 2, 1: 2, 2: 2, 3: 2},
        'metric': {0: fs.fit,
                   1: fs.fit,
                   2: fs.fit,
                   3: fs.fit},
        'n_total_conditions': {0: 3, 1: 3, 2: 4, 3: 4},
        'tree_ensemble': {0: RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
                          1: RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
                          2: RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
                          3: RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0)},
        'precision_threshold': {0: 0, 1: 0, 2: 0, 3: 0},
        'num_cores': {0: 1, 1: 1, 2: 1, 3: 1},
        'target_feat_corr_types': {0: 'Infer', 1: 'Infer', 2: 'Infer', 3: 'Infer'},
        'Performance': {0: 0.2564102564102564,
                        1: 0.2564102564102564,
                        2: 0.26315789473684215,
                        3: 0.26315789473684215}
    })
    param_results_per_fold.index.name = 'ParamSetIndex'
    expected_param_results_aggregated = pd.DataFrame({
        'metric': {0: fs.fit,
                   1: fs.fit,
                   2: fs.fit,
                   3: fs.fit},
        'n_total_conditions': {0: 3, 1: 3, 2: 4, 3: 4},
        'tree_ensemble': {0: RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
                          1: RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0),
                          2: RandomForestClassifier(max_depth=4, n_estimators=10, random_state=0),
                          3: RandomForestClassifier(max_depth=4, n_estimators=50, random_state=0)},
        'precision_threshold': {0: 0, 1: 0, 2: 0, 3: 0},
        'num_cores': {0: 1, 1: 1, 2: 1, 3: 1},
        'target_feat_corr_types': {0: 'Infer', 1: 'Infer', 2: 'Infer', 3: 'Infer'},
        'PerformancePerFold': {0: np.array([0.08130081, 0.35714286, 0.25641026]),
                               1: np.array([0.26315789, 0.35714286, 0.25641026]),
                               2: np.array([0.2173913, 0.45454545, 0.26315789]),
                               3: np.array([0.43478261, 0.57692308, 0.26315789])},
        'MeanPerformance': {0: 0.23161797552041452,
                            1: 0.2922370027633186,
                            2: 0.3116982178767076,
                            3: 0.42495452678519036},
        'StdDevPerformance': {0: 0.11396842025139182,
                              1: 0.04597796650063309,
                              2: 0.10272177622711993,
                              3: 0.12828247680703012}}
    )
    expected_param_results_aggregated.index.name = 'ParamSetIndex'
    param_results_aggregated = gs._calculate_aggregated_perf(
        param_results_per_fold=param_results_per_fold, param_combinations=param_combinations)
    assert all(param_results_aggregated['PerformancePerFold']
               == param_results_aggregated['PerformancePerFold'])
    assert all(param_results_aggregated['MeanPerformance']
               == param_results_aggregated['MeanPerformance'])
    assert all(param_results_aggregated['StdDevPerformance']
               == param_results_aggregated['StdDevPerformance'])


def test_train_rules_using_params(create_data,
                                  instantiate_gs_cv, params):
    X, y, _ = create_data
    gs = instantiate_gs_cv
    params = params
    X_rules, rg = gs._train_rules_using_params(
        rule_class=RuleGeneratorDT, params=params, X=X, y=y,
        sample_weight=None)
    assert X_rules.sum().sum() == 4469
    assert isinstance(rg, RuleGeneratorDT)
