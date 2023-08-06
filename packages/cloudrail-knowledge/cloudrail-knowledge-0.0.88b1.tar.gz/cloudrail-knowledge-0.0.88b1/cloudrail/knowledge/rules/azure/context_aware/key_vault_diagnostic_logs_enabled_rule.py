from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class KeyVaultDiagnosticLogsEnabledRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'car_key_vault_diagnostic_logs_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for key_vault in env_context.key_vaults:
            if \
                    not key_vault.monitor_diagnostic_settings \
                    or not key_vault.monitor_diagnostic_settings.logs_settings \
                    or not key_vault.monitor_diagnostic_settings.logs_settings.enabled \
                    or not key_vault.monitor_diagnostic_settings.logs_settings.retention_policy \
                    or not key_vault.monitor_diagnostic_settings.logs_settings.retention_policy.enabled:
                issues.append(
                    Issue(
                        f'The Key Vault `{key_vault.name}` does not have diagnostic logs enabled.',
                        key_vault,
                        key_vault))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.key_vaults)
