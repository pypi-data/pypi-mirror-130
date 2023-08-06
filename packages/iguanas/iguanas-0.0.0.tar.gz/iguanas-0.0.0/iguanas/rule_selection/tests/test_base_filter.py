import pytest
import pandas as pd
from iguanas.rule_selection._base_filter import _BaseFilter


@pytest.fixture
def _create_data():
    X_rules = pd.DataFrame({
        'A': [1, 0, 1],
        'B': [1, 1, 1]
    })
    rule_descriptions = pd.DataFrame([
        ['A', 0.1, 0.2],
        ['B', 0.1, 0.2]
    ],
        columns=['Rule', 'Precision', 'Recall']
    )
    rule_descriptions.set_index('Rule', inplace=True)
    return X_rules, rule_descriptions


def test_transform(_create_data):
    X_rules, rule_descriptions = _create_data
    bf = _BaseFilter(rule_descriptions=None)
    bf.rules_to_keep = ['A']
    X_rules_ = bf.transform(X_rules)
    pd.testing.assert_frame_equal(X_rules_, X_rules[['A']])
    assert bf.rule_descriptions is None
    bf = _BaseFilter(rule_descriptions=rule_descriptions)
    bf.rules_to_keep = ['A']
    X_rules_ = bf.transform(X_rules)
    pd.testing.assert_frame_equal(X_rules_, X_rules[['A']])
    pd.testing.assert_frame_equal(
        bf.rule_descriptions, rule_descriptions.loc[['A']])


def test_fit_transform(_create_data):
    bf = _BaseFilter
    # Just create dummy fit function for testing
    bf.fit = lambda self, X_rules, y, sample_weight: None
    X_rules, rule_descriptions = _create_data
    bf = _BaseFilter(rule_descriptions=None)
    bf.rules_to_keep = ['A']
    X_rules_ = bf.fit_transform(X_rules)
    pd.testing.assert_frame_equal(X_rules_, X_rules[['A']])
    assert bf.rule_descriptions is None
    bf = _BaseFilter(rule_descriptions=rule_descriptions)
    bf.rules_to_keep = ['A']
    X_rules_ = bf.fit_transform(X_rules)
    pd.testing.assert_frame_equal(X_rules_, X_rules[['A']])
    pd.testing.assert_frame_equal(
        bf.rule_descriptions, rule_descriptions.loc[['A']])
