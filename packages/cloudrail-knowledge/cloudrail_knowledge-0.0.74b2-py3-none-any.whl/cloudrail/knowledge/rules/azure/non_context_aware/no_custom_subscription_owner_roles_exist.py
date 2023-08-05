from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class NoCustomSubscriptionOwnerRolesExist(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_no_custom_subscription_owner_roles_exist'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.role_definitions)

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for role_definition in env_context.role_definitions:
            if any('*' in permission.actions for permission in role_definition.permissions) and \
                    ['/subscriptions/' in scope for scope in role_definition.scopes]:
                issues.append(Issue(f'The custom role `{role_definition.name}` has subscription owner permissions',
                                    role_definition,
                                    role_definition))
        return issues
