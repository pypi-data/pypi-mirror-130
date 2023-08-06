"""
Unit tests for methods in _base_generator module that aren't specific to Pandas 
or Koalas
"""
import pytest
from iguanas.rule_generation import RuleGeneratorDT
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import fbeta_score


@pytest.fixture
def fs_instantiated():
    class FScore:
        def __init__(self, beta):
            self.beta = beta

        def fit(self, y_true, y_pred, sample_weight):
            return fbeta_score(y_true=y_true, y_pred=y_pred, beta=self.beta, sample_weight=sample_weight, zero_division=0)
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


def test_convert_conditions_to_string(rg_instantiated):
    list_of_conditions = [
        ('A', '>=', 1),
        ('B', '<=', 1.5),
        ('C', '==', 1),
        ('D', '<=', 2.9),
        ('E', '>', 0.5)
    ]
    columns_int = ['B', 'C', 'E']
    columns_cat = ['C', 'E']
    rg, _ = rg_instantiated
    rule_name = rg._convert_conditions_to_string(
        list_of_conditions, columns_int, columns_cat)
    assert rule_name == "(X['A']>=1)&(X['B']<=1)&(X['C']==True)&(X['D']<=2.9)&(X['E']==True)"


def test_clean_dup_features_from_conditions(rg_instantiated):
    list_of_conditions = [
        ('A', '>=', 1),
        ('A', '>=', 3),
        ('B', '<=', 2),
        ('B', '<=', 1),
        ('C', '>', 0.5),
        ('C', '<=', 1)
    ]
    expected_result = [
        ('A', '>=', 3),
        ('B', '<=', 1),
        ('C', '<=', 1),
        ('C', '>', 0.5)
    ]
    rg, _ = rg_instantiated
    result = rg._clean_dup_features_from_conditions(list_of_conditions)
    assert result == expected_result


def test_generate_rule_name(rg_instantiated):
    rg, _ = rg_instantiated
    rule_name = rg._generate_rule_name_dt()
    assert rule_name == 'RGDT_Rule_20200204_0'
    rg.rule_name_prefix = 'TEST'
    rule_name = rg._generate_rule_name_dt()
    assert rule_name == 'TEST_1'


def test_remove_misaligned_conditions(rg_instantiated):
    target_feat_corr_types = {
        'PositiveCorr': ['ColA'],
        'NegativeCorr': ['ColB'],
    }
    branch_conditions = [
        ('ColA', '>=', 1),
        ('ColA', '<=', 5),
        ('ColB', '>=', 1),
        ('ColB', '<=', 5),
    ]
    expected_result = [('ColA', '>=', 1), ('ColB', '<=', 5)]
    rg, _ = rg_instantiated
    cleaned_branch_conditions = rg._remove_misaligned_conditions(
        branch_conditions=branch_conditions,
        target_feat_corr_types=target_feat_corr_types
    )
    assert all([a == b for a, b in zip(
        cleaned_branch_conditions, expected_result)])
