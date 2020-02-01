import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="vpc_postgres",
    version="0.0.1",

    description="Python CDK - VPC + Postgres",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # tweaks from https://github.com/aws-samples/aws-cdk-examples/tree/master/python/new-vpc-alb-asg-mysql
    author="Martin Peters",

    package_dir={"": "stacks"},
    packages=setuptools.find_packages(where="stacks"),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-elasticloadbalancingv2",
        "aws-cdk.aws-autoscaling",
        "aws-cdk.aws-rds",
        "aws-cdk.aws-secretsmanager",
        "aws-cdk.aws-lambda",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-cloudwatch"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
