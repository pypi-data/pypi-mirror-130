import importlib
import argparse
import json
import os
import subprocess
import sys
import random
import errno

from pyspark.sql import SparkSession
from pyspark import SparkFiles

random.seed()

class ServerChannel:
    def __init__(self, run_dir):
        self.run_dir = run_dir

    def read_json(self, spark, name):
        with open(os.path.join(self.run_dir, name), "r") as f:
            return json.load(f)

    def has_json(self, spark, name):
        return os.path.isfile(os.path.join(self.run_dir, name))

    def write_json(self, spark, name, payload):
        with open(os.path.join(self.run_dir, name), "w") as f:
            json.dump(payload, f)

    def delete_json(self, spark, name):
        os.remove(os.path.join(self.run_dir, name))

# lib installer
def _install_libs(run_home):
    print(f"job_loader._install_libs: enter, run_home = {run_home}")

    lib_zip     = SparkFiles.get("lib.zip")
    lib_dir     = os.path.join(run_home, "python_libs")
    lock_name   = os.path.join(run_home, '__lock__')

    for i in range(0, 100):
        try:
            lock_fh = os.open(lock_name, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(lock_fh)
            try:
                if not os.path.isdir(lib_dir):
                    print("_install_libs: install lib starts")
                    os.makedirs(lib_dir)
                    subprocess.check_call(['unzip', "-qq", lib_zip, "-d", lib_dir])
                    print("_install_libs: install lib done")
                if lib_dir not in sys.path:
                    print(f"_install_libs: add {lib_dir} path")
                    sys.path.insert(0, lib_dir)
                print("job_loader._install_libs: exit")
                return
            finally:
                os.remove(lock_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                time.sleep(random.randint(1, 10))
                continue
            raise

    raise Exception("Failed to install libraries!")


def _bootstrap():
    parser = argparse.ArgumentParser(description='job')
    parser.add_argument(
        "--run-id", type=str, required=True, help="Run ID",
    )
    parser.add_argument(
        "--run-dir", type=str, required=True, help="Run Directory",
    )
    parser.add_argument(
        "--app-dir", type=str, required=True, help="Application Directory",
    )
    parser.add_argument(
        "--enable-aws-s3",
        help="Allow pyspark to access aws s3 buckets",
        action="store_true",
    )
    parser.add_argument(
        "--aws-account", type=str, required=False, help="AWS Account json file",
    )
    parser.add_argument(
        "--aws-s3-buffer-dir", type=str, required=False, help="AWS S3 buffer dir",
    )
    args = parser.parse_args()
    spark = SparkSession.builder.appName(f"RunJob-{args.run_id}").getOrCreate()

    if args.enable_aws_s3:
        hadoop_conf = spark._jsc.hadoopConfiguration()
        hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        if args.aws_s3_buffer_dir is not None:
            hadoop_conf.set("fs.s3.buffer.dir", args.aws_s3_buffer_dir)

        if args.aws_account is not None:
            with open(args.aws_account, "rt") as f:
                aws_account_content = json.load(f)
            hadoop_conf.set("fs.s3.awsAccessKeyId", aws_account_content['aws_access_key_id'])
            hadoop_conf.set("fs.s3.awsSecretAccessKey", aws_account_content['aws_secret_access_key'])


    sc = spark.sparkContext
    sc.addPyFile(os.path.join(args.app_dir, "app.zip"))
    sc.addFile(os.path.join(args.app_dir, 'lib.zip'))

    print(f"run-id:  {args.run_id}")
    print(f"run-dir: {args.run_dir}")
    print(f"app-dir: {args.app_dir}")

    run_home = os.path.join(args.run_dir, args.run_id)
    print(f"run-home: {run_home}")

    # setup lib path
    _install_libs(run_home)

    # load input args
    with open(os.path.join(run_home, "input.json"), "r") as f:
        input_args = json.load(f)


    try:
        entry = importlib.import_module("main")
        result = entry.main(spark, input_args, sysops={
            "install_libs": lambda : _install_libs(run_home),
            "channel": ServerChannel(os.path.join(args.run_dir, args.run_id))
        })

        # save output
        with open(os.path.join(run_home, "result.json"), "w") as out_f:
            json.dump(result, out_f)

    finally:
        spark.stop()

_bootstrap()

