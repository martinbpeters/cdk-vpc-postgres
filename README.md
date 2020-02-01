# Python CDK with VPC + Postgres DB

## Installation

### Python virtual environment
```
virtualenv aws_cdk.env
cd aws_cdk.env
source bin/activate
```

### Install AWS CDK 
```
npm install -g aws-cdk
cdk --version
cdk --help
```
No harm to read up the docs: https://docs.aws.amazon.com/cdk

Install the dependencies:
```
pip install aws-cdk.aws-s3
pip install aws-cdk.aws-ec2
pip install aws-cdk.aws-rds
pip install aws-cdk.aws-events-targets
pip install -r requirements.txt
```

New versions come available, no harm in keeping up to date:
```
pip install --upgrade aws-cdk.core
pip install --upgrade aws-cdk.aws-s3
pip install --upgrade aws-cdk.aws-ec2
pip install --upgrade aws-cdk.aws-rds
pip install --upgrade aws-cdk.aws-events-targets
```

Set up your AWS profile file ~/.aws/config
```
[profile cdk_profile]
aws_access_key_id=AKIAI44QH8DHBEXAMPLE
aws_secret_access_key=je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
region=eu-west-1
```

Synthesizing the stacks. --no-version-reporting removes the `AWS::CDK::Metadata` resources and opts out of 
module version reporting to AWS.
. 
```
cdk --profile cdk_profile --no-version-reporting synth VPC AuroraServerless PostgresRDS
```

Deploying the stacks
```
cdk --profile cdk_profile --no-version-reporting deploy VPC AuroraServerless PostgresRDS
```

Destroy the stacks
```
cdk --profile cdk_profile --no-version-reporting destroy VPC AuroraServerless PostgresRDS
```

Debugging a stack
```
cdk --profile cdk_profile --no-version-reporting synth VPC  > vpc.yaml
aws cloudformation validate-template --template-body file://vpc.yaml 
```

## CDK Examples
https://github.com/aws-samples/aws-cdk-examples/tree/master/python

https://github.com/aws-samples/aws-cdk-examples/tree/master/python/new-vpc-alb-asg-mysql
https://github.com/aws-samples/aws-aurora-serverless-data-api-sam/blob/master/deploy_scripts/rds_cfn_template.yaml

## CDK Python API
https://docs.aws.amazon.com/cdk/api/latest/python 
https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html
https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-readme.html

## Blogs
https://blog.codecentric.de/en/2019/09/aws-cdk-create-custom-vpc/
https://blog.codecentric.de/en/2019/10/aws-cdk-part-2-s3-bucket/
https://blog.codecentric.de/en/2019/09/aws-cdk-versus-terraform-and-serverless-framework/

https://stackoverflow.com/questions/55818680/how-to-set-dbparametergroup-family-property-for-postgres-10-6/55818740

https://sanderknape.com/2019/05/building-serverless-applications-aws-cdk/

https://labs.consol.de/development/2019/11/04/introduction-to-aws-cdk.html

https://jimmydqv.com/aws/cloudformation/infrastructure/cdk/2019/08/14/aws-cdk-first-impression.html

https://dev.to/hoangleitvn/top-reasons-why-we-use-aws-cdk-over-cloudformation-2b2f

https://aws.amazon.com/blogs/aws/new-data-api-for-amazon-aurora-serverless/
https://madabout.cloud/2019/09/01/aws-data-api-for-amazon-aurora-serverless/
https://read.acloud.guru/getting-started-with-the-amazon-aurora-serverless-data-api-6b84e466b109

## Docs 
https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.html
https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/

## Tools
https://studio.infviz.io/

## CIDR Blocks
http://jodies.de/ipcalc?host=10.0.0.0&mask1=16&mask2=
https://cloudacademy.com/course/aws-virtual-private-cloud-subnets-and-routing/vpc-cidr-blocks/

## Aurora Serverless 
https://github.com/chanzuckerberg/sqlalchemy-aurora-data-api
https://www.npmjs.com/package/@cfn-modules/rds-aurora-serverless-postgres

https://stackoverflow.com/questions/51879688/creating-an-aurora-serverless-cluster-from-cloudformation
https://stackoverflow.com/questions/59409935/create-cfndbcluster-in-non-default-vpc?rq=1