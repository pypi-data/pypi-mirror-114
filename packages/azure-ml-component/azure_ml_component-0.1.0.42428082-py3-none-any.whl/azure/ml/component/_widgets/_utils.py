# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.core import Workspace, Experiment
from .._restclients.service_caller_factory import _DesignerServiceCallerFactory

SUBSCRIPTION_ID = 'subscriptionId'
RESOURCE_GROUP = 'resourceGroup'
WORKSPACE_NAME = 'workspaceName'

cached_workspace_by_wsid = {}


def _get_pipeline_run_from_content(content):
    run_id = content.get("runId")
    subscription_id = content.get("subscriptionId")
    resource_group = content.get("resourceGroup")
    workspace_name = content.get("workspaceName")
    experiment_name = content.get("experimentName")

    workspace = Workspace.get(subscription_id=subscription_id,
                              resource_group=resource_group,
                              name=workspace_name)
    experiment = Experiment(workspace, experiment_name)

    from azure.ml.component import Run
    return Run(experiment, run_id)


def get_designer_service_caller_from_dict(paras_dict):
    if SUBSCRIPTION_ID not in paras_dict or RESOURCE_GROUP not in paras_dict or WORKSPACE_NAME not in paras_dict:
        return None
    subscription_id = paras_dict[SUBSCRIPTION_ID]
    resource_group = paras_dict[RESOURCE_GROUP]
    workspace_name = paras_dict[WORKSPACE_NAME]
    wsid = '{}/{}/{}'.format(subscription_id, resource_group, workspace_name)
    ws = cached_workspace_by_wsid.get(
        wsid,
        Workspace(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name))
    cached_workspace_by_wsid[wsid] = ws
    service_caller = _DesignerServiceCallerFactory.get_instance(ws)
    return service_caller
