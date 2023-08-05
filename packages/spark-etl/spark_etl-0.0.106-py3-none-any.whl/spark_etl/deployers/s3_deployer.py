import os
from urllib.parse import urlparse
import json

from .abstract_deployer import AbstractDeployer
from spark_etl import Build
from spark_etl.exceptions import SparkETLDeploymentFailure

import boto3

class S3Deployer(AbstractDeployer):
    """
    This deployer deploys application to AWS S3 buckets
    """
    def __init__(self, config):
        super(S3Deployer, self).__init__(config)


    def deploy(self, build_dir, deployment_location):
        o = urlparse(deployment_location)
        if o.scheme not in ('s3', 's3a'):
            raise SparkETLDeploymentFailure("deployment_location must be in s3 or s3a")

        build = Build(build_dir)

        args = {}
        if 'aws_account' in self.config:
            with open(
                os.path.expandvars(os.path.expanduser(self.config['aws_account'])),
                "rt"
            ) as f:
                aws_account_content     = json.load(f)
                args['aws_access_key_id']       = aws_account_content['aws_access_key_id']
                args['aws_secret_access_key']   = aws_account_content['aws_secret_access_key']
        else:
            if 'aws_access_key_id' in self.config:
                args['aws_access_key_id']       = self.config['aws_access_key_id']
                args['aws_secret_access_key']   = self.config['aws_secret_access_key']


        s3_client = boto3.client('s3', **args)
        bucket_name = o.netloc
        s3_dirname = os.path.join(o.path[1:], build.version)

        print(f"Upload to AWS s3, bucket name = {bucket_name}")
        for artifact in build.artifacts:
            local_filename = os.path.join(build.build_dir, artifact)
            object_name = os.path.join(s3_dirname, artifact)

            print(f"{local_filename}  ==> {object_name}")
            s3_client.upload_file(local_filename, bucket_name, object_name)


        local_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'job_loader.py')
        object_name = os.path.join(s3_dirname, "job_loader.py")
        print(f"{local_filename}  ==> {object_name}")
        s3_client.upload_file(local_filename, bucket_name, object_name)

