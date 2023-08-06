# -*- coding: utf-8 -*-
import os
import re
import sys
from typing import Optional
from urllib.parse import unquote_plus, urlparse
from uuid import UUID

from apistar.exceptions import ErrorResponse
from rich import print
from rich.progress import Progress

from arkindex_cli.auth import Profiles

SIMPLE_URL_REGEX = re.compile("^http(s)?://")


def add_iiif_parser(subcommands):
    iiif_parser = subcommands.add_parser(
        "iiif-images",
        description="Create elements on a corpus grouped by prefix from a list of IIIF paths.",
        help="Create elements on a corpus grouped by prefix from a list of IIIF paths.",
    )
    iiif_parser.add_argument(
        "input_file",
        help="Path to a local file containing IIIF images complete URIs, one by line.",
    )
    iiif_parser.add_argument(
        "corpus_id",
        help="UUID of the corpus to import images to.",
        type=UUID,
    )
    iiif_parser.add_argument(
        "--import-folder-name",
        help="Name of the main folder created to contain imported elements.",
        default="IIIF import",
    )
    iiif_parser.add_argument(
        "--import-folder-type",
        help="Type of the main folder created to contain imported elements.",
        default="folder",
    )
    iiif_parser.add_argument(
        "--element-type",
        help="type of elements created from IIIF paths.",
        default="page",
    )
    iiif_parser.add_argument(
        "--image-name-delimiter",
        help=(
            "Delimit the last part of the image URL path that should be used for the imported element name. "
            "Defaults to '/'."
        ),
        default="/",
    )
    iiif_parser.add_argument(
        "--group-prefix-delimiter",
        help="If defined, create sub-folders containing IIIF images grouped by a similar name prefix.",
    )
    iiif_parser.add_argument(
        "--group-folder-type",
        help=(
            "Type for sub-folders containing grouped IIIF images. "
            "This parameter requires prefix delimiter to be defined."
        ),
    )
    iiif_parser.set_defaults(func=run)


def create_element(client, corpus_id, name, elt_type, **kwargs):
    """
    Perform the creation of an element
    """
    try:
        return client.request(
            "CreateElement",
            body={"corpus": str(corpus_id), "name": name, "type": elt_type, **kwargs},
        )
    except ErrorResponse as e:
        print(
            "[bright_red]"
            f"Failed creating {elt_type} '{name}': {e.status_code} - {e.content}."
        )
        print("Aborting.")
        sys.exit(2)


def run(
    input_file: str,
    corpus_id: UUID,
    import_folder_name: str,
    import_folder_type: str,
    element_type: str,
    image_name_delimiter: Optional[str] = "/",
    group_prefix_delimiter: Optional[str] = None,
    group_folder_type: Optional[str] = None,
    profile_slug: Optional[str] = None,
) -> int:
    """
    Create elements in a corpus from a list of IIIF paths.
    A single folder will be created at the root of the corpus, with optional name and type.
    Sub-folders could be created to group images by prefix if .
    """

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Loading API client")
        profiles = Profiles()
        profile = profiles.get_or_exit(profile_slug)
        client = profiles.get_api_client(profile)

    import_folder = create_element(
        client, str(corpus_id), import_folder_name, import_folder_type
    )
    corpus_name = import_folder["corpus"].get("name", "—")
    print(
        f"Created import {import_folder_type} '{import_folder_name}' in corpus '{corpus_name}'"
    )

    group_folders = {}
    for iiif_path in open(input_file, "r").readlines():
        # Import and organize elements for each IIIF image
        iiif_url = iiif_path.strip()
        if not SIMPLE_URL_REGEX.match(iiif_url):
            # URI seems to be invalid
            print(f"[bright_yellow]Invalid IIIF url '{iiif_url}'. Skipping")
            continue

        print(f"Processing {iiif_url}")
        # iiif_url = urllib.parse.quote_plus(iiif_path)
        image = None
        try:
            image = client.request("CreateIIIFURL", body={"url": iiif_url})
            print(f"Created a new image on Arkindex - '{image['id']}'")
        except ErrorResponse as e:
            if e.status_code == 400 and "id" in e.content:
                # In case the image already exists, we retrieve its full information
                image = client.request("RetrieveImage", id=e.content["id"])
                print(f"Retrieved an existing image on Arkindex - '{image['id']}'")
            else:
                print(
                    "[bright_yellow]"
                    f"Failed creating iiif image {iiif_url}: {e.status_code} - {e.content}. Skipping"
                )
                continue

        path = urlparse(iiif_path).path
        # Unquote to handle a proper image name
        path = unquote_plus(path)
        image_name, _ext = os.path.splitext(path.split(image_name_delimiter)[-1])

        parent = import_folder
        if group_prefix_delimiter:
            # Retrieve or create the group folder for this image
            group_name = image_name.split(group_prefix_delimiter)[0]
            if group_name not in group_folders:
                group_folders[group_name] = create_element(
                    client,
                    corpus_id,
                    group_name,
                    # Use default import folder type if groups type is undefined
                    group_folder_type or import_folder_type,
                    parent=import_folder["id"],
                )
            parent = group_folders[group_name]

        # Create the final element for this image
        create_element(
            client,
            corpus_id,
            image_name,
            element_type,
            parent=parent["id"],
            image=image["id"],
        )
        print(f"Successfully created element {image_name} for image {iiif_url}")
