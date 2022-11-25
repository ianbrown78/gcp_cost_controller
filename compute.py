from typing import Iterable
import google
from google.cloud import compute_v1

class GoogleComputeEngine:

    instance_client = None

    def __init__(self, credentials: google.auth.credentials.Credentials):
        if credentials == None:
            self.instance_client = compute_v1.InstancesClient()
        else:
            self.instance_client = compute_v1.InstancesClient(credentials)

    
    def list_instances(self, project_id: str, zone: str) -> Iterable[compute_v1.Instance]:
        """
        List all instances in the given zone in the specified project.

        Args:
            project_id: project ID or project number of the Cloud project you want to use.
            zone: name of the zone you want to use.
        Returns:
            An iterable collection of Instance objects.
        """
        return self.instance_client.list(project=project_id, zone=zone)

    
    def filter_by_label(self, instances: Iterable[compute_v1.Instance], label: str, value: str):
        """
        Returns a filtered list of instances based on the label name and value.

        Args:
            instances: Iterable[compute_v1.Instance]
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

    
    def start_stop_instance(self, instance: compute_v1.Instance, project: str, zone: str, action: str):
        """
        Start or Stop the named instance

        Args:
            instance: compute_v1.instance to start/stop
            project_id: project ID or project number of the Cloud project you want to use.
            zone: name of the zone you want to use.
        Returns:
            A instance start/stop response
        """
        if action.lower == 'start':
            return self.instance_client.start(project=project, zone=zone, instance=instance, timeout=30)
        elif action.lower == 'stop':
            return self.instance_client.stop(project=project, zone=zone, instance=instance, timeout=30)
        else:
            return 
