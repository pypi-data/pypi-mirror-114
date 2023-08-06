from typing import List, Optional
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class VpcGatewayAttachment(AwsResource):

    def __init__(self, attachment_id: str, region: str, account: str, igw_id: str, vpc_id: str, vpn_gw_id: str):
        AwsResource.__init__(self, account, region)
        self.attachment_id: str = attachment_id
        self.igw_id: str = igw_id
        self.vpc_id: str = vpc_id
        self.vpn_gw_id: str = vpn_gw_id
        self.with_aliases(attachment_id)

    def get_keys(self) -> List[str]:
        return [self.attachment_id]

    def get_id(self) -> str:
        return self.attachment_id

    @property
    def is_tagable(self) -> bool:
        return False

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        pass
