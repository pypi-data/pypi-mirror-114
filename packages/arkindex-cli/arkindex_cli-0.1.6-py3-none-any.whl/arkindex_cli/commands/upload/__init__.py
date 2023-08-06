# -*- coding: utf-8 -*-
from arkindex_cli.commands.upload.iiif import add_iiif_parser
from arkindex_cli.commands.upload.minio_client import add_minio_client_parser


def add_upload_parser(subcommands) -> None:
    upload_parser = subcommands.add_parser(
        "upload",
        description="Upload data to Arkindex",
        help="Upload data to Arkindex",
    )
    subparsers = upload_parser.add_subparsers()
    add_iiif_parser(subparsers)
    add_minio_client_parser(subparsers)

    def subcommand_required(*args, **kwargs):
        upload_parser.error("A subcommand is required.")

    upload_parser.set_defaults(func=subcommand_required)
