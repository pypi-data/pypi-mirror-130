import pytest
from iguanas.rule_selection import CorrelatedFilter
from iguanas.metrics import FScore, CosineSimilarity, JaccardSimilarity
from iguanas.correlation_reduction import AgglomerativeClusteringReducer
import iguanas.utils as utils
import numpy as np
import pandas as pd
import random
from itertools import product
from iguanas.rule_application import RuleApplier


@pytest.fixture
def create_data():
    np.random.seed(0)
    X = pd.DataFrame(
        np.random.randint(0, 10, (1000, 10)),
        columns=[f'col{i}' for i in range(10)]
    )
    y = pd.Series(np.random.randint(0, 2, 1000))
    rule_descriptions = utils.return_rule_descriptions_from_X_rules(
        X, X.columns, y, None, None
    )
    return X, y, rule_descriptions


@pytest.fixture
def expected_columns_to_keep():
    return [
        ['col8', 'col9'],
        ['col0', 'col1'],
        ['col8', 'col4'],
        ['col6', 'col0'],
        ['col8'],
        ['col0'],
        ['col8'],
        ['col0'],
        ['col0', 'col1', 'col2', 'col3', 'col4',
            'col5', 'col6', 'col7', 'col8', 'col9'],
        ['col0', 'col1', 'col2', 'col3', 'col4',
            'col5', 'col6', 'col7', 'col8', 'col9'],
        ['col8', 'col4'],
        ['col6', 'col0'],
        ['col0', 'col1', 'col2', 'col3', 'col4',
            'col5', 'col6', 'col7', 'col8', 'col9'],
        ['col0', 'col1', 'col2', 'col3', 'col4',
            'col5', 'col6', 'col7', 'col8', 'col9'],
        ['col8'],
        ['col0'],
    ]


def test_fit(create_data, expected_columns_to_keep):
    X_rules, y, rule_descriptions = create_data
    expected_results = expected_columns_to_keep
    cs = CosineSimilarity()
    js = JaccardSimilarity()
    fs = FScore(0.5)
    combinations = list(
        product([0.25, 0.75], ['top_down', 'bottom_up'], [cs.fit, js.fit], [fs.fit, None]))
    for i, (threshold, strategy, similarity_function, metric) in enumerate(combinations):
        crc = AgglomerativeClusteringReducer(
            threshold=threshold, strategy=strategy,
            similarity_function=similarity_function,
            metric=metric
        )
        fr = CorrelatedFilter(
            correlation_reduction_class=crc, rule_descriptions=rule_descriptions
        )
        if metric is None:
            fr.fit(X_rules=X_rules)
        else:
            print(type(y))
            fr.fit(X_rules=X_rules, y=y)
        assert fr.rules_to_keep == expected_results[i]


def test_transform(create_data, expected_columns_to_keep):
    X_rules, y, rule_descriptions = create_data
    expected_results = expected_columns_to_keep
    cs = CosineSimilarity()
    js = JaccardSimilarity()
    fs = FScore(0.5)
    combinations = list(
        product([0.25, 0.75], ['top_down', 'bottom_up'], [cs.fit, js.fit], [fs.fit, None]))
    for i, (threshold, strategy, similarity_function, metric) in enumerate(combinations):
        crc = AgglomerativeClusteringReducer(
            threshold=threshold, strategy=strategy,
            similarity_function=similarity_function,
            metric=metric
        )
        crc_wo_rd = AgglomerativeClusteringReducer(
            threshold=threshold, strategy=strategy,
            similarity_function=similarity_function,
            metric=metric
        )
        fr = CorrelatedFilter(
            correlation_reduction_class=crc, rule_descriptions=rule_descriptions
        )
        fr_wo_rd = CorrelatedFilter(
            correlation_reduction_class=crc_wo_rd
        )
        if metric is None:
            fr.fit(X_rules=X_rules)
            fr_wo_rd.fit(X_rules=X_rules)
        else:
            fr.fit(X_rules=X_rules, y=y)
            fr_wo_rd.fit(X_rules=X_rules, y=y)
        X_rules_reduced = fr.transform(X_rules=X_rules)
        X_rules_wo_rd_reduced = fr_wo_rd.transform(X_rules=X_rules)
        assert fr.rules_to_keep == X_rules_reduced.columns.tolist(
        ) == fr.rule_descriptions.index.tolist() == expected_results[i]
        assert fr_wo_rd.rules_to_keep == X_rules_wo_rd_reduced.columns.tolist(
        ) == expected_results[i]


def test_fit_transform(create_data, expected_columns_to_keep):
    X_rules, y, rule_descriptions = create_data
    expected_results = expected_columns_to_keep
    cs = CosineSimilarity()
    js = JaccardSimilarity()
    fs = FScore(0.5)
    combinations = list(
        product([0.25, 0.75], ['top_down', 'bottom_up'], [cs.fit, js.fit], [fs.fit, None]))
    for i, (threshold, strategy, similarity_function, metric) in enumerate(combinations):
        crc = AgglomerativeClusteringReducer(
            threshold=threshold, strategy=strategy,
            similarity_function=similarity_function,
            metric=metric
        )
        crc_wo_rd = AgglomerativeClusteringReducer(
            threshold=threshold, strategy=strategy,
            similarity_function=similarity_function,
            metric=metric
        )
        fr = CorrelatedFilter(
            correlation_reduction_class=crc, rule_descriptions=rule_descriptions
        )
        fr_wo_rd = CorrelatedFilter(
            correlation_reduction_class=crc_wo_rd
        )
        if metric is None:
            X_rules_reduced = fr.fit_transform(X_rules=X_rules)
            X_rules_wo_rd_reduced = fr_wo_rd.fit_transform(X_rules=X_rules)
        else:
            X_rules_reduced = fr.fit_transform(X_rules=X_rules, y=y)
            X_rules_wo_rd_reduced = fr_wo_rd.fit_transform(
                X_rules=X_rules, y=y)
        assert fr.rules_to_keep == X_rules_reduced.columns.tolist(
        ) == fr.rule_descriptions.index.tolist() == expected_results[i]
        assert fr_wo_rd.rules_to_keep == X_rules_wo_rd_reduced.columns.tolist(
        ) == expected_results[i]
