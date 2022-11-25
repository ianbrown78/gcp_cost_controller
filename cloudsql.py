from googleapiclient import discovery
import google.auth

class GoogleCloudSql:
    instance_client = None

    def __init__(self, credentials: google.auth.credentials.Credentials):
        self.instance_client = googleapiclient.discovery.build('sqladmin', 'v1beta4', credentials=credentials)

    def list_instances(self, project_id: str):
        return self.instance_client.instances().list(project_id=project_id)

    def filter_by_label(self, instances: list, label: str, value: str):
        """
        Returns a filtered list of instances based on the label name and value.

        Args:
            instances: list
            label: The label to search for
            value: The value the label needs to contain.
        Returns:
            An iterable collection of Instance objects.
        """
        filtered_instances = []
        for instance in instances:
            if label in instance.labels:
                if value == instance.labels[label]:
                    filtered_instances.append(instance)

        return filtered_instances

    def start_stop_instance(self, instance: str, project: str, action: str):
        
        if action.lower == 'start':
            policy = 'ALWAYS'
        elif action.lower == 'stop':
            policy = 'NEVER'

        request = {
            "settings": {
                "activationPolicy": policy
            }
        }

        request = self.instance_client.instances().patch(
            project=project,
            instance=instance,
            body=request).execute()

        return request
