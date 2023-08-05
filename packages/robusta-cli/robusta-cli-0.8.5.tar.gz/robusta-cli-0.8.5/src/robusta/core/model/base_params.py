from pydantic import BaseModel
from typing import Dict, Any, List


class GenParams(BaseModel):
    name: str
    params: Dict[Any, Any] = {}


class SlackParams(BaseModel):
    slack_channel: str


class NodeNameParams(BaseModel):
    node_name: str = None


class PodParams(BaseModel):
    pod_name: str = None
    pod_namespace: str = None


class BashParams(BaseModel):
    bash_command: str


class NamespacedKubernetesObjectParams(BaseModel):
    name: str = None
    namespace: str = None


class PrometheusParams(BaseModel):
    prometheus_url: str = None
