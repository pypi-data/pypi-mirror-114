#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import os
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote_plus

from minio import Minio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s/%(name)s: %(message)s"
)
logger = logging.getLogger(os.path.basename(__file__))

MINIO_ACCESS_KEY_NAME = "MINIO_ACCESS_KEY"
MINIO_SECRET_KEY_NAME = "MINIO_SECRET_KEY"


class MinioClient:
    def __init__(self, bucket_name, out_dir, iiif_server, minio_url):
        self.bucket_name = bucket_name
        self.out_dir = out_dir
        self.IIIF_SERVER = iiif_server

        # Create client with access and secret key.
        for required_env in [MINIO_ACCESS_KEY_NAME, MINIO_SECRET_KEY_NAME]:
            assert (
                required_env in os.environ
            ), f"{required_env} env variable must be defined"

        minio_access_key = os.environ[MINIO_ACCESS_KEY_NAME]
        minio_secret_key = os.environ[MINIO_SECRET_KEY_NAME]

        self.client = Minio(minio_url, minio_access_key, minio_secret_key)

        self.out_dir.mkdir(parents=True, exist_ok=True)

    def print_bucket_names(self):
        bucket_names = "\n".join([bucket.name for bucket in self.client.list_buckets()])
        logger.info(f"Available bucket names: {bucket_names}")

    def create_iiif_urls_by_parent(self):
        """
        Create iiif urls grouped by the first level parent objects in minio bucket
        """
        iiif_urls_by_parent = defaultdict(list)
        for obj in self.client.list_objects(self.bucket_name, recursive=True):
            obj_name = obj.object_name
            if "/" in obj_name:
                parent = obj_name.split("/")[0]
            else:
                logger.info("Flat file structure, using bucket as parent")
                parent = self.bucket_name

            iiif_path = f"{self.bucket_name}/{obj_name}"
            iiif_url = self.IIIF_SERVER + quote_plus(iiif_path.strip())

            iiif_urls_by_parent[parent].append(iiif_url)
        return iiif_urls_by_parent

    def write_iiif_urls_to_files(self, iiif_urls_by_parent):
        """
        Save each iiif urls group into a separate file
        """
        for parent, iiif_urls in iiif_urls_by_parent.items():
            out_file = (self.out_dir / parent).with_suffix(".txt")
            with open(out_file, "w") as f:
                f.write("\n".join(iiif_urls))

    def run(self):
        iiif_urls = self.create_iiif_urls_by_parent()
        self.write_iiif_urls_to_files(iiif_urls)


def run(self, **kwargs):
    MinioClient(**kwargs).run()


def add_minio_client_parser(subcommands):
    minio_parser = subcommands.add_parser(
        "minio",
        description="Get IIIF urls by parent from Minio",
        help="Get IIIF urls by parent from Minio",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    minio_parser.add_argument(
        "-b",
        "--bucket_name",
        type=str,
        required=True,
        help="Name of the bucket on Minio",
    )
    minio_parser.add_argument(
        "-o",
        "--out_dir",
        type=Path,
        default=Path("iiif_urls_output/"),
        help="Directory where the output files will be created",
    )
    minio_parser.add_argument(
        "--iiif_server",
        type=str,
        default="https://iiif-europe.teklia.com/iiif/2/",
        help="IIIF server url",
    )
    minio_parser.add_argument(
        "--minio_url", type=str, default="storage.teklia.com", help="Minio server url"
    )
    minio_parser.set_defaults(func=run)
