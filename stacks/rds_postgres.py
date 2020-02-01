from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_lambda as _lambda,
    aws_events_targets as targets,
    aws_cloudwatch as cloudwatch,
    core
)


class RDSPostgresStack(core.Stack):
    """

    """
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db = rds.DatabaseInstance(
            self,
            id="RDSPostgresDB",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            engine_version="11",
            instance_class=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
            master_username="admin",
            vpc=vpc,
            vpc_placement=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.ISOLATED
            ),
            multi_az=True,
            allocated_storage=100,
            storage_type=rds.StorageType.GP2,
            cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
            deletion_protection=False,
            delete_automated_backups=False,
            backup_retention=core.Duration.days(7),
            parameter_group=rds.ParameterGroup.from_parameter_group_name(
                self,
                id="para-group-postgres",
                parameter_group_name="postgres11"
            )
        )

        # Rotate the master user password every 30 days
        db.add_rotation_single_user()

        # Add alarm for high CPU
        cloudwatch.Alarm(
            self,
            id="HighCPU",
            metric=db.metric_cpu_utilization(),
            threshold=90,
            evaluation_periods=1
        )

        # Trigger Lambda function on instance availability events
        fn = _lambda.Function(self,
            id="PostgresAvailibilityFunction",
            code=_lambda.Code.from_inline("exports.handler = (event) => console.log(event);"),
            handler="index.handler",
            runtime=_lambda.Runtime.NODEJS_10_X
        )

        availability_rule = db.on_event(
            "Availability",
            target=targets.LambdaFunction(fn))

        availability_rule.add_event_pattern(
            detail={
                "EventCategories": [
                    "availability"
                ]
            }
        )