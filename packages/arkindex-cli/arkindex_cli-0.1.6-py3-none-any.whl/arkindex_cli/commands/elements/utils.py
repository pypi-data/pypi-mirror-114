# -*- coding: utf-8 -*-
from uuid import UUID

from arkindex_cli.utils import ask


def get_children_list(client, **kwargs):
    """
    Get a list of element UUID from:
    - one single UUID passed in the command
    - a file (one UUID per line)
    - the selection on Arkindex
    - the pages in a corpus that do not have a parent folder element
    """

    uuid_list = kwargs.get("uuid_list", None)
    child = kwargs.get("child", None)
    selection = kwargs.get("selection", False)
    stray_pages = kwargs.get("stray_pages", False)
    parent_element = kwargs.get("parent_element", None)

    if uuid_list is not None:
        children = [line.strip() for line in open(uuid_list, "r").readlines()]
        assert (
            len(children) > 0
        ), "The list of element UUIDs could not be recovered. Check your input file."
    elif child is not None:
        children = [child]
        assert len(children) > 0, "No child element UUID was given."
    elif selection:
        children = [item["id"] for item in client.paginate("ListSelection")]
        assert len(children) > 0, "The selection on Arkindex is empty."
    elif stray_pages:
        children = []
        corpus_id = parent_element["corpus"]["id"]
        all_pages = client.paginate("ListElements", corpus=corpus_id, type="page")
        for one_page in all_pages:
            page_parents = client.request(
                "ListElementParents", id=one_page["id"], folder=True
            )
            if page_parents["count"] == 0:
                children.append(one_page["id"])
        assert len(children) > 0, f"There are no stray pages in corpus {corpus_id}."
    else:
        raise ValueError(
            "A single UUID, file, Arkindex selection or 'stray-pages' is required as child(ren) input."
        )
    return children


def get_parent_element(parent, create, client):
    """
    - Retrieve an existing element information from its UUID
    - Create a new element and return its information
    """
    if parent is not None:
        parent_element = client.request("RetrieveElement", id=parent)
    elif create:
        parent_corpus = UUID(
            ask("Enter the UUID of the corpus in which to create the element").strip()
        )
        parent_type = ask("Enter the element type of the element to create").strip()

        # checking that the specified type exists in the specified corpus
        if not any(
            item["slug"] == parent_type
            for item in client.request("RetrieveCorpus", id=parent_corpus)["types"]
        ):
            raise ValueError(
                f"Element type {parent_type} does not exist in corpus {parent_corpus}."
            )
        parent_name = ask("Enter the name of the element to create").strip()
        body = {"type": parent_type, "corpus": str(parent_corpus), "name": parent_name}
        parent_element = client.request("CreateElement", body=body)
    else:
        raise ValueError("An element UUID or 'create' is required as parent input.")
    return parent_element
