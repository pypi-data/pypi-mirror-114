from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.security.azure_security_center_subscription_pricing import SubscriptionPricingResourceType, \
    SubscriptionPricingTier
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class DefenderForContainerRegistriesEnabledRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_container_registries_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for subscription_pricing in env_context.security_center_subscription_pricings:
            if subscription_pricing.resource_type == SubscriptionPricingResourceType.CONTAINER_REGISTRY and \
                    subscription_pricing.tier != SubscriptionPricingTier.STANDARD:
                issues.append(
                    Issue(
                        f'Azure Defender is not enabled for container registries in the subscription `{subscription_pricing.subscription_id}`.',
                        subscription_pricing,
                        subscription_pricing))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.security_center_subscription_pricings)
