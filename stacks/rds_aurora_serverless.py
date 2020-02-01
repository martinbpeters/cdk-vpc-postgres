from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as sm,
    core
)


class AuroraServerlessStack(core.Stack):
    """

    """
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_master_user_name="admin_user"

        secret = rds.DatabaseSecret(
            self,
            id="MasterUserSecret",
            username=db_master_user_name
        )

        subnet_ids = []
        for subnet in vpc.isolated_subnets:
            subnet_ids.append(subnet.subnet_id)

        subnet_group = rds.CfnDBSubnetGroup(
            self,
            id="AuroraServerlessSubnetGroup",
            db_subnet_group_description='Aurora Postgres Serverless Subnet Group',
            subnet_ids=subnet_ids,
            db_subnet_group_name='auroraserverlesssubnetgroup' # needs to be all lowercase
        )

        db_cluster_name="aurora-serverless-postgres-db"

        security_group = ec2.SecurityGroup(
            self,
            id="SecurityGroup",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(ec2.Peer.ipv4('10.0.0.0/16'), ec2.Port.tcp(5432), "allow psql through")

        self.db = rds.CfnDBCluster(
            self,
            id="AuroraServerlessDB",
            engine=rds.DatabaseClusterEngine.AURORA_POSTGRESQL.name,
            engine_mode="serverless",
            db_subnet_group_name=subnet_group.db_subnet_group_name,

            vpc_security_group_ids=[security_group.security_group_id],
            availability_zones=vpc.availability_zones,

            db_cluster_identifier=db_cluster_name,
            #db_cluster_parameter_group_name=

            database_name="slsdb",
            master_username=secret.secret_value_from_json("username").to_string(),
            master_user_password=secret.secret_value_from_json("password").to_string(),

            port=5432,

            deletion_protection=False,
            scaling_configuration=rds.CfnDBCluster.ScalingConfigurationProperty(
                auto_pause=True,
                min_capacity=2,
                max_capacity=16,
                seconds_until_auto_pause=300
            ),

            enable_cloudwatch_logs_exports=[
                "error",
                "general",
                "slowquery",
                "audit"
            ],
            enable_http_endpoint=True
            #kms_key_id=
            #tags=
        )
        self.db.node.add_dependency(subnet_group)
        self.db.node.add_dependency(security_group)

        #secret_attached = secret.attach(target=self)
        #secret.add_target_attachment(id="secret_attachment", target=self.db)

        secret_attached = sm.CfnSecretTargetAttachment(
            self,
            id="secret_attachment",
            secret_id=secret.secret_arn,
            target_id=self.db.ref,
            target_type="AWS::RDS::DBCluster",
        )
        secret_attached.node.add_dependency(self.db)

        core.CfnOutput(
            self,
            id="StackName",
            value=self.stack_name,
            description="Stack Name",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:stack-name"
        )

        core.CfnOutput(
            self,
            id="DatabaseName",
            value=self.db.database_name,
            description="Database Name",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:database-name"
        )

        core.CfnOutput(
            self,
            id="DatabaseClusterArn",
            value=f"arn:aws:rds:{self.region}:{self.account}:cluster:{self.db.ref}",
            description="Database Cluster Arn",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:database-cluster-arn"
        )

        core.CfnOutput(
            self,
            id="DatabaseSecretArn",
            value=secret.secret_arn,
            description="Database Secret Arn",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:database-secret-arn"
        )

        core.CfnOutput(
            self,
            id="DatabaseClusterID",
            value=self.db.db_cluster_identifier,
            description="Database Cluster Id",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:database-cluster-id"
        )

        core.CfnOutput(
            self,
            id="AuroraEndpointAddress",
            value=self.db.attr_endpoint_address,
            description="Aurora Endpoint Address",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:aurora-endpoint-address"
        )

        core.CfnOutput(
            self,
            id="DatabaseMasterUserName",
            value=db_master_user_name,
            description="Database Master User Name",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:database-master-username"
        )
