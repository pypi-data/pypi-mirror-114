from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureRoleDefinitionPermission:
    def __init__(self, actions: List[str], not_actions: List[str]):
        self.actions = actions
        self.not_actions = not_actions


class AzureRoleDefinition(AzureResource):

    def __init__(self, role_id: str, name: str, scopes: List[str], description: str, permissions: List[AzureRoleDefinitionPermission]) -> None:
        super().__init__(AzureResourceType.AZURERM_ROLE_DEFINITION)
        self.id = role_id
        self.name = name
        self.scopes = scopes
        self.description = description
        self.permissions = permissions

    def get_keys(self) -> List[str]:
        return [self.name]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
