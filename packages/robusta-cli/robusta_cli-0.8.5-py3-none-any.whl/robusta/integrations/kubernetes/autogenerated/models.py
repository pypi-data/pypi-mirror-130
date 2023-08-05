# This file was autogenerated. Do not edit.

from .v1.models import KIND_TO_MODEL_CLASS as v1
from .v2beta1.models import KIND_TO_MODEL_CLASS as v2beta1
from .v2beta2.models import KIND_TO_MODEL_CLASS as v2beta2

VERSION_KIND_TO_MODEL_CLASS = {"v1": v1, "v2beta1": v2beta1, "v2beta2": v2beta2}


def get_api_version(apiVersion: str):
    if "/" in apiVersion:
        apiVersion = apiVersion.split("/")[1]
    return VERSION_KIND_TO_MODEL_CLASS.get(apiVersion)
