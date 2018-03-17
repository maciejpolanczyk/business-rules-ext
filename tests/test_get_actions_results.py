from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, boolean_rule_variable
from business_rules.engine import run_all, get_value, InvalidRuleDefinition
from . import TestCase


class ActionsResultsClassTests(TestCase):
    """ Test methods on getting fired rules actions results
    """
    def test_should_get_all_actions_results(self):
        result = run_all(**self._get_params_for_run_all())
        self.assertEqual(
            result,
            [
                {'some_action_1': 'fooValue'},
                {'some_action_2': 'foobarValue', 'some_action_3': None},
            ]
        )

    def test_should_get_only_first_action_result(self):
        result = run_all(**self._get_params_for_run_all(), stop_on_first_trigger=True)
        self.assertEqual(result, [{'some_action_1': 'fooValue'}])

    def test_should_get_value(self):
        result = get_value(**self._get_params_for_run_all())
        expected = 'fooValue'
        self.assertEqual(result, expected)

    def test_should_raise_exception_when_more_than_one_action_executed(self):
        params = self._get_params_for_run_all()
        params['rule_list'] = [
            {
                'conditions': {'all': [
                    {
                        'name': 'this_is_rule_2',
                        'value': True,
                        'operator': 'is_false'
                    }]
                },
                'actions': [
                    {'name': 'some_action_2', 'params': {'foobar': 'foobarValue'}},
                    {'name': 'some_action_3'}
                ]
            }
        ]
        expected_message = 'Expected only one action to be executed.'
        with self.assertRaisesRegex(InvalidRuleDefinition, expected_message):
            get_value(**params)

    def test_should_raise_exception_when_none_action_executed(self):
        params = self._get_params_for_run_all()
        params['rule_list'] = [
            {
                'conditions': {'all': [
                    {
                        'name': 'this_is_rule_1',
                        'value': True,
                        'operator': 'is_true'
                    }]
                },
                'actions': []
            }
        ]
        expected_message = 'No rule executed or no action found in matching rule'
        with self.assertRaisesRegex(InvalidRuleDefinition, expected_message):
            get_value(**params)

    def test_should_raise_exception_when_none_rule_triggered(self):
        params = self._get_params_for_run_all()
        params['rule_list'] = []
        expected_message = 'No rule executed or no action found in matching rule'
        with self.assertRaisesRegex(InvalidRuleDefinition, expected_message):
            get_value(**params)

    @staticmethod
    def _get_params_for_run_all():
        class SomeVariables(BaseVariables):
            @boolean_rule_variable
            def this_is_rule_1(self):
                return True

            @boolean_rule_variable
            def this_is_rule_2(self):
                return False

        class SomeActions(BaseActions):
            @rule_action(params={'foo': FIELD_TEXT})
            def some_action_1(self, foo):
                return foo

            @rule_action(params={'foobar': FIELD_TEXT})
            def some_action_2(self, foobar):
                return foobar

            @rule_action()
            def some_action_3(self):
                pass

        rule1 = {
            'conditions': {'all': [
                {
                    'name': 'this_is_rule_1',
                    'value': True,
                    'operator': 'is_true'
                }]
            },
            'actions': [{'name': 'some_action_1', 'params': {'foo': 'fooValue'}}]
        }
        rule2 = {
            'conditions': {'all': [
                {
                    'name': 'this_is_rule_2',
                    'value': True,
                    'operator': 'is_false'
                }]
            },
            'actions': [
                {'name': 'some_action_2', 'params': {'foobar': 'foobarValue'}},
                {'name': 'some_action_3'}
            ]
        }

        variables = SomeVariables()
        actions = SomeActions()

        return {
            'rule_list': [rule1, rule2],
            'defined_variables': variables,
            'defined_actions': actions,
        }
