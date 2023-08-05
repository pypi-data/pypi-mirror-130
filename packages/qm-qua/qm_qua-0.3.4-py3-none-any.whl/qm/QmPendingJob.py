import time
from datetime import datetime
from typing import Optional

from qm.QmJob import QmJob
from qm._errors import JobCancelledError
from qm.pb.frontend_pb2 import GetJobExecutionStatusRequest


class QmPendingJob(object):
    """
    A Class describing a job in the execution queue
    """

    def __init__(
        self,
        job_id,
        machine: "qm.QuantumMachine.QuantumMachine",
        qmm: "qm.QuantumMachinesManager.QuantumMachinesManager",
    ):

        self._id = job_id
        self._machine = machine
        self._qmm = qmm
        self._added_user_id = None
        self._time_added = None
        self._set_metadata()

    def _set_metadata(self):
        response = self._get_execution_status()
        if response.status.HasField("pending"):
            self._added_user_id = response.status.pending.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.pending.timeAdded.seconds
            )
        elif response.status.HasField("running"):
            self._added_user_id = response.status.running.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.running.timeAdded.seconds
            )
        elif response.status.HasField("completed"):
            self._added_user_id = response.status.completed.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.completed.timeAdded.seconds
            )
        elif response.status.HasField("loading"):
            self._added_user_id = response.status.loading.addedBy
            self._time_added = datetime.fromtimestamp(
                response.status.loading.timeAdded.seconds
            )

    def id(self) -> str:
        """
        :return: The id of the job

        """
        return self._id

    @property
    def user_added(self):
        return self._added_user_id

    @property
    def time_added(self) -> datetime:
        return self._time_added

    def position_in_queue(self) -> Optional[int]:
        """
        Returns the current position of the job in the queue

        :return: The position in the queue

        Example:

            >>> pending_job.position_in_queue()

        """
        response = self._get_execution_status()
        if response.status.HasField("pending"):
            return response.status.pending.positionInQueue
        return None  # Job left queue

    def _get_execution_status(self):
        request = GetJobExecutionStatusRequest()
        request.quantumMachineId = self._machine.id
        request.jobId = self._id
        response = self._qmm._frontend.GetJobExecutionStatus(request)
        return response

    def wait_for_execution(self, timeout: Optional[float] = None) -> QmJob:
        """
        Waits for a job to complete or until the timeout has elapsed

        :param timeout: Timeout (in seconds) for this operation

        :return: The completed ``QmJob``

        """
        start = time.time()
        end = start + max(0.0, timeout) if timeout is not None else None

        while end is None or time.time() < end:
            response = self._get_execution_status()
            if response.status.HasField("pending") or response.status.HasField(
                "loading"
            ):
                time.sleep(0.02)
            elif response.status.HasField("running") or response.status.HasField(
                "completed"
            ):
                return QmJob(self._qmm, self._id, None)
            else:
                raise JobCancelledError(f"job {self._id} was cancelled")
        raise TimeoutError(f"job {self._id} was not started in time")

    def cancel(self) -> bool:
        """
        Removes the job from the queue

        :return: true if the operation was successful

        Example:

            >>> pending_job.cancel()

        """
        return self._machine.queue.remove_by_id(self._id) > 0
