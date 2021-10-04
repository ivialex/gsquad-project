#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from gsquad_project.gsquad_project_stack import GsquadProjectStack


app = core.App()
GsquadProjectStack(app,
                   "GsquadProjectStack",
                   vpc_id='vpc-02a6ddb92f37e0c6c',
                   account_id='028186285749',
                   availability_zones=['us-east-1a', 'us-east-1b'],
                   private_subnet_ids=['subnet-0ef26b6fca166d338', 'subnet-0dc2ac1917efe844d'],
                   public_subnet_ids=['subnet-06410b721d3925f36', 'subnet-0502d7209cdeb9f11'],
                   env={'account': os.environ['CDK_DEFAULT_ACCOUNT'],
                          'region': os.environ['CDK_DEFAULT_REGION']
                        }
    )

app.synth()
