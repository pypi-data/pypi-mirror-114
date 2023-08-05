#!/usr/bin/python
# -*- coding: utf-8 -*-
"""GCP Secret Managerから値を取得する

Python 3.7+に対応

"""
from __future__ import annotations
from google.cloud import secretmanager

PROJECT_ID = None


def set_project_id(project_id: str | None = None):
    global PROJECT_ID
    if project_id is None:
        from get_metadata import get_metadata

        PROJECT_ID = get_metadata("project_id")
    else:
        PROJECT_ID = project_id


def get_secret_text_from_env(
    env_secret_name: str, env_secret_ver: str | None = None
) -> str | None:
    from os import getenv

    secret_name = getenv(env_secret_name, None)
    if secret_name is None:
        return None

    if env_secret_ver is None:
        secret_ver = "latest"
    else:
        secret_ver = getenv(env_secret_ver, "latest")

    return get_secret_text(secret_name, secret_ver)


def get_secret_text(secret_name: str, secret_ver: str | int = "latest"):
    """
    プロジェクトID、シークレット名、シークレットのバージョンを指定して
    Secret Manager から情報を取得する
    """
    global PROJECT_ID

    if PROJECT_ID is None:
        set_project_id()

    if PROJECT_ID is None:
        return None

    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(PROJECT_ID, secret_name, str(secret_ver))
    # print(f"get secret text {name=}")
    response = client.access_secret_version(name=name)

    return response.payload.data.decode("UTF-8")
