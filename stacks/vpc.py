from aws_cdk import (
    aws_ec2 as ec2,
    core
)

ec2_type = "t3.micro"
key_name = "id_rsa"  # Setup key_name for EC2 instance login

with open("./user_data/bastion.sh") as f:
    user_data = f.read()

class VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id="VPC",
            cidr="10.0.0.0/16",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(
                    name="private", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PRIVATE),
                ec2.SubnetConfiguration(
                    name="DB", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.ISOLATED
                ),
                # ec2.SubnetConfiguration(
                #     name="DB2", cidr_mask=24,
                #     reserved=False, subnet_type=ec2.SubnetType.ISOLATED
                # )
            ],
            enable_dns_hostnames=True,
            enable_dns_support=True
        )

        core.Tag(key="Application", value="AWS::StackName") \
            .add(self.vpc, key="Application", value="AWS::StackName")
        # core.Tag("Network", "Public").add(vpc)
        # core.Tag("Name", "VPCName-Environment").add(vpc)
        # core.Tag("Environment", "Environment").add(vpc)

        bastion = ec2.BastionHostLinux(
            self,
            id="BastionHost",
            vpc=self.vpc,
            instance_name="BastionHost",
            instance_type=ec2.InstanceType(ec2_type),
            subnet_selection=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )
        bastion.allow_ssh_access_from(ec2.Peer.any_ipv4())

        # Setup key_name for EC2 instance login if you don't use Session Manager
        #bastion.instance.instance.add_property_override("KeyName", key_name)

        ec2.CfnEIP(self, id="BastionHostEIP", domain="vpc", instance_id=bastion.instance_id)

        core.CfnOutput(
            self,
            id="VPCId",
            value=self.vpc.vpc_id,
            description="VPC ID",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:vpc-id"
        )

        core.CfnOutput(
            self,
            id="BastionPrivateIP",
            value=bastion.instance_private_ip,
            description="BASTION Private IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:bastion-private-ip"
        )

        core.CfnOutput(
            self,
            id="BastionPublicIP",
            value=bastion.instance_public_ip,
            description="BASTION Public IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:bastion-public-ip"
        )
