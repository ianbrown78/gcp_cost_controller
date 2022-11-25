import base64
import os
import sys
from google.cloud import secretmanager_v1
from cloudsql import GoogleCloudSql
from compute import GoogleComputeEngine

"""
All calls need to come through the main function.
We should be receiving:
- r = type of resource to control (One of compute or cloudsql)
- p = project id to run this against
- z = zone to use (only for compute)
- l = label to look for on the resource
- v = value we should match against on that label
- a = action to take against all matching instances. (One of start or stop)
"""
def main(request):
    if request.args and 'r' in request.args:
        resource_type = request.args.get('r')
    if request.args and 'project' in request.args:
        project_id = request.args.get('project')
    if request.args and 'zone' in request.args:
        zone = request.args.get('zone')
    if request.args and 'label' in request.args:
        label = request.args.get('label')
    if request.args and 'value' in request.args:
        value = request.args.get('value')
    if request.args and 'action' in request.args:
        action = request.args.get('action')

    # Create the Secret Manager client.
    secrets_client = secretmanager_v1.SecretManagerServiceClient()
    secret_name = os.getenv('secret_name')
    secret_response = secrets_client.access_secret_version(name=f"projects/{project_id}/secrets/{secret_name}/versions/latest")
    secret_payload = secret_response.payload.data.decode("UTF-8")

    if resource_type == 'compute':
        handle_compute_actions(project_id, zone, label, value, action, secret_payload)
    elif resource_type == 'cloudsql':
        handle_cloudsql_actions(project_id, label, value, action, secret_payload)


def handle_compute_actions(project, zone, label, value, action, secret_payload):
    # create new class
    compute_client = GoogleComputeEngine(secret_payload)

    # list all instances
    instances = compute_client.list_instances()

    # find instances to control by label & value
    filtered_instances = compute_client.filter_by_label(instances, label, value)

    # perform action
    for i in range(len(filtered_instances)):
        output = compute_client.start_stop_instance(filtered_instances[i], project, zone, action)
        sys.stdout.write(output)

def handle_cloudsql_actions(project, label, value, action, secret_payload):
    # create new class
    cloudsql_client = GoogleCloudSql(secret_payload)

    # list all instances
    instances = cloudsql_client.list_instances()

    # find instances to control by label & value
    filtered_instances = cloudsql_client.filter_by_label(instances, label, value)

    # perform action
    for i in range(len(filtered_instances)):
        output = cloudsql_client.start_stop_instance(filtered_instances[i], project, action)
        sys.stdout.write(output)