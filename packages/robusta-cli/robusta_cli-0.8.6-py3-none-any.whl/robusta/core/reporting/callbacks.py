import time
from pydantic import BaseModel

from robusta.core.reporting.action_requests import (
    sign_action_request,
    ExternalActionRequest,
    ActionRequestBody,
)
from . import CallbackChoice
from ..playbooks.actions_registry import ActionsRegistry


class ExternalActionRequestBuilder(BaseModel):
    @classmethod
    def create_for_func(
        cls,
        choice: CallbackChoice,
        sink: str,
        text: str,
        account_id: str,
        cluster_name: str,
        signing_key: str,
    ):
        if choice.action is None:
            raise Exception(
                f"The callback for choice {text} is None. Did you accidentally pass `foo()` as a callback and not `foo`?"
            )
        if not ActionsRegistry.is_playbook_action(choice.action):
            raise Exception(
                f"{choice.action} is not a function that was decorated with @action"
            )

        if not signing_key:
            raise Exception(
                f"Cannot create callback request with no signing key. Configure signing_key in globalConfig"
            )
        action_params = (
            {} if choice.action_params is None else choice.action_params.dict()
        )
        body = ActionRequestBody(
            account_id=account_id,
            cluster_name=cluster_name,
            timestamp=time.time(),
            action_name=choice.action.__name__,
            action_params=action_params,
            sinks=[sink],
            origin="callback",
        )
        return ExternalActionRequest(
            body=body,
            signature=sign_action_request(body, signing_key),
        )
