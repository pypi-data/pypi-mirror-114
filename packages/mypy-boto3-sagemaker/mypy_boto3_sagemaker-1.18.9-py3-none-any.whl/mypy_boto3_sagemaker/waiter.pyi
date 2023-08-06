"""
Type annotations for sagemaker service client waiters.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_sagemaker import SageMakerClient
    from mypy_boto3_sagemaker.waiter import (
        EndpointDeletedWaiter,
        EndpointInServiceWaiter,
        NotebookInstanceDeletedWaiter,
        NotebookInstanceInServiceWaiter,
        NotebookInstanceStoppedWaiter,
        ProcessingJobCompletedOrStoppedWaiter,
        TrainingJobCompletedOrStoppedWaiter,
        TransformJobCompletedOrStoppedWaiter,
    )

    client: SageMakerClient = boto3.client("sagemaker")

    endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
    endpoint_in_service_waiter: EndpointInServiceWaiter = client.get_waiter("endpoint_in_service")
    notebook_instance_deleted_waiter: NotebookInstanceDeletedWaiter = client.get_waiter("notebook_instance_deleted")
    notebook_instance_in_service_waiter: NotebookInstanceInServiceWaiter = client.get_waiter("notebook_instance_in_service")
    notebook_instance_stopped_waiter: NotebookInstanceStoppedWaiter = client.get_waiter("notebook_instance_stopped")
    processing_job_completed_or_stopped_waiter: ProcessingJobCompletedOrStoppedWaiter = client.get_waiter("processing_job_completed_or_stopped")
    training_job_completed_or_stopped_waiter: TrainingJobCompletedOrStoppedWaiter = client.get_waiter("training_job_completed_or_stopped")
    transform_job_completed_or_stopped_waiter: TransformJobCompletedOrStoppedWaiter = client.get_waiter("transform_job_completed_or_stopped")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "EndpointDeletedWaiter",
    "EndpointInServiceWaiter",
    "NotebookInstanceDeletedWaiter",
    "NotebookInstanceInServiceWaiter",
    "NotebookInstanceStoppedWaiter",
    "ProcessingJobCompletedOrStoppedWaiter",
    "TrainingJobCompletedOrStoppedWaiter",
    "TransformJobCompletedOrStoppedWaiter",
)

class EndpointDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.EndpointDeleted)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#endpointdeletedwaiter)
    """

    def wait(self, *, EndpointName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.EndpointDeleted.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#endpointdeletedwaiter)
        """

class EndpointInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.EndpointInService)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#endpointinservicewaiter)
    """

    def wait(self, *, EndpointName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.EndpointInService.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#endpointinservicewaiter)
        """

class NotebookInstanceDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceDeleted)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstancedeletedwaiter)
    """

    def wait(self, *, NotebookInstanceName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceDeleted.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstancedeletedwaiter)
        """

class NotebookInstanceInServiceWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceInService)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstanceinservicewaiter)
    """

    def wait(self, *, NotebookInstanceName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceInService.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstanceinservicewaiter)
        """

class NotebookInstanceStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceStopped)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstancestoppedwaiter)
    """

    def wait(self, *, NotebookInstanceName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.NotebookInstanceStopped.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#notebookinstancestoppedwaiter)
        """

class ProcessingJobCompletedOrStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#processingjobcompletedorstoppedwaiter)
    """

    def wait(self, *, ProcessingJobName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#processingjobcompletedorstoppedwaiter)
        """

class TrainingJobCompletedOrStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.TrainingJobCompletedOrStopped)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#trainingjobcompletedorstoppedwaiter)
    """

    def wait(self, *, TrainingJobName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.TrainingJobCompletedOrStopped.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#trainingjobcompletedorstoppedwaiter)
        """

class TransformJobCompletedOrStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.TransformJobCompletedOrStopped)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#transformjobcompletedorstoppedwaiter)
    """

    def wait(self, *, TransformJobName: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.9/reference/services/sagemaker.html#SageMaker.Waiter.TransformJobCompletedOrStopped.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/waiters.html#transformjobcompletedorstoppedwaiter)
        """
