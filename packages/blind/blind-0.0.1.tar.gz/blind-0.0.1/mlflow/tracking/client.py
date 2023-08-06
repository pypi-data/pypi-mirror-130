"""
Internal package providing a Python CRUD interface to MLflow experiments, runs, registered models,
and model versions. This is a lower level API than the :py:mod:`mlflow.tracking.fluent` module,
and is exposed in the :py:mod:`mlflow.tracking` module.
"""
import logging

from mlflow.entities import ViewType
from mlflow.store.tracking import SEARCH_MAX_RESULTS_DEFAULT
from mlflow.tracking._tracking_service import utils
from mlflow.tracking._tracking_service.client import TrackingServiceClient

_logger = logging.getLogger(__name__)


class MlflowClient(object):
    """
    Client of an MLflow Tracking Server that creates and manages experiments and runs, and of an
    MLflow Registry Server that creates and manages registered models and model versions. It's a
    thin wrapper around TrackingServiceClient and RegistryClient so there is a unified API but we
    can keep the implementation of the tracking and registry clients independent from each other.
    """

    def __init__(self, tracking_uri=None, registry_uri=None):
        """
        :param tracking_uri: Address of local or remote tracking server. If not provided, defaults
                             to the service set by ``mlflow.tracking.set_tracking_uri``. See
                             `Where Runs Get Recorded <../tracking.html#where-runs-get-recorded>`_
                             for more info.
       """
        final_tracking_uri = utils._resolve_tracking_uri(tracking_uri)
        self._tracking_client = TrackingServiceClient(final_tracking_uri)
        # `MlflowClient` also references a `ModelRegistryClient` instance that is provided by the
        # `MlflowClient._get_registry_client()` method. This `ModelRegistryClient` is not explicitly
        # defined as an instance variable in the `MlflowClient` constructor; an instance variable
        # is assigned lazily by `MlflowClient._get_registry_client()` and should not be referenced
        # outside of the `MlflowClient._get_registry_client()` method

    # Tracking API

    def get_run(self, run_id):
        """
        Fetch the run from backend store. The resulting :py:class:`Run <mlflow.entities.Run>`
        contains a collection of run metadata -- :py:class:`RunInfo <mlflow.entities.RunInfo>`,
        as well as a collection of run parameters, tags, and metrics --
        :py:class:`RunData <mlflow.entities.RunData>`. In the case where multiple metrics with the
        same key are logged for the run, the :py:class:`RunData <mlflow.entities.RunData>` contains
        the most recently logged value at the largest step for each metric.

        :param run_id: Unique identifier for the run.

        :return: A single :py:class:`mlflow.entities.Run` object, if the run exists. Otherwise,
                 raises an exception.

        .. code-block:: python
            :caption: Example

            import mlflow
            from mlflow.tracking import MlflowClient

            with mlflow.start_run() as run:
                mlflow.log_param("p", 0)

            # The run has finished since we have exited the with block
            # Fetch the run
            client = MlflowClient()
            run = client.get_run(run.info.run_id)
            print("run_id: {}".format(run.info.run_id))
            print("params: {}".format(run.data.params))
            print("status: {}".format(run.info.status))

        .. code-block:: text
            :caption: Output

            run_id: e36b42c587a1413ead7c3b6764120618
            params: {'p': '0'}
            status: FINISHED
        """
        return self._tracking_client.get_run(run_id)

    def get_metric_history(self, run_id, key):
        """
        Return a list of metric objects corresponding to all values logged for a given metric.

        :param run_id: Unique identifier for run
        :param key: Metric name within the run

        :return: A list of :py:class:`mlflow.entities.Metric` entities if logged, else empty list

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_metric_info(history):
                for m in history:
                    print("name: {}".format(m.key))
                    print("value: {}".format(m.value))
                    print("step: {}".format(m.step))
                    print("timestamp: {}".format(m.timestamp))
                    print("--")

            # Create a run under the default experiment (whose id is "0"). Since this is low-level
            # CRUD operation, the method will create a run. To end the run, you'll have
            # to explicitly end it.
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            print("run_id: {}".format(run.info.run_id))
            print("--")

            # Log couple of metrics, update their initial value, and fetch each
            # logged metrics' history.
            for k, v in [("m1", 1.5), ("m2", 2.5)]:
                client.log_metric(run.info.run_id, k, v, step=0)
                client.log_metric(run.info.run_id, k, v + 1, step=1)
                print_metric_info(client.get_metric_history(run.info.run_id, k))
            client.set_terminated(run.info.run_id)

        .. code-block:: text
            :caption: Output

            run_id: c360d15714994c388b504fe09ea3c234
            --
            name: m1
            value: 1.5
            step: 0
            timestamp: 1603423788607
            --
            name: m1
            value: 2.5
            step: 1
            timestamp: 1603423788608
            --
            name: m2
            value: 2.5
            step: 0
            timestamp: 1603423788609
            --
            name: m2
            value: 3.5
            step: 1
            timestamp: 1603423788610
            --
        """
        return self._tracking_client.get_metric_history(run_id, key)

    def create_run(self, experiment_id, start_time=None, tags=None):
        """
        Create a :py:class:`mlflow.entities.Run` object that can be associated with
        metrics, parameters, artifacts, etc.
        Unlike :py:func:`mlflow.projects.run`, creates objects but does not run code.
        Unlike :py:func:`mlflow.start_run`, does not change the "active run" used by
        :py:func:`mlflow.log_param`.

        :param experiment_id: The string ID of the experiment to create a run in.
        :param start_time: If not provided, use the current timestamp.
        :param tags: A dictionary of key-value pairs that are converted into
                     :py:class:`mlflow.entities.RunTag` objects.
        :return: :py:class:`mlflow.entities.Run` that was created.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create a run with a tag under the default experiment (whose id is '0').
            tags = {"engineering": "ML Platform"}
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id, tags=tags)

            # Show newly created run metadata info
            print("Run tags: {}".format(run.data.tags))
            print("Experiment id: {}".format(run.info.experiment_id))
            print("Run id: {}".format(run.info.run_id))
            print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
            print("status: {}".format(run.info.status))

        .. code-block:: text
            :caption: Output

            Run tags: {'engineering': 'ML Platform'}
            Experiment id: 0
            Run id: 65fb9e2198764354bab398105f2e70c1
            lifecycle_stage: active
            status: RUNNING
        """
        return self._tracking_client.create_run(experiment_id, start_time, tags)

    def list_run_infos(
        self,
        experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """:return: List of :py:class:`mlflow.entities.RunInfo`

        .. code-block:: python
            :caption: Example

            import mlflow
            from mlflow.tracking import MlflowClient
            from mlflow.entities import ViewType

            def print_run_infos(run_infos):
                for r in run_infos:
                    print("- run_id: {}, lifecycle_stage: {}".format(r.run_id, r.lifecycle_stage))

            # Create two runs
            with mlflow.start_run() as run1:
                mlflow.log_metric("click_rate", 1.55)

            with mlflow.start_run() as run2:
                mlflow.log_metric("click_rate", 2.50)

            # Delete the last run
            client = MlflowClient()
            client.delete_run(run2.info.run_id)

            # Get all runs under the default experiment (whose id is 0)
            print("Active runs:")
            print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ACTIVE_ONLY))

            print("Deleted runs:")
            print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.DELETED_ONLY))

            print("All runs:")
            print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ALL,
                            order_by=["metric.click_rate DESC"]))

        .. code-block:: text
            :caption: Output

            Active runs:
            - run_id: 47b11b33f9364ee2b148c41375a30a68, lifecycle_stage: active
            Deleted runs:
            - run_id: bc4803439bdd4a059103811267b6b2f4, lifecycle_stage: deleted
            All runs:
            - run_id: bc4803439bdd4a059103811267b6b2f4, lifecycle_stage: deleted
            - run_id: 47b11b33f9364ee2b148c41375a30a68, lifecycle_stage: active
        """
        return self._tracking_client.list_run_infos(
            experiment_id, run_view_type, max_results, order_by, page_token
        )

    def list_experiments(self, view_type=None):
        """
        :return: List of :py:class:`mlflow.entities.Experiment`

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient
            from mlflow.entities import ViewType

            def print_experiment_info(experiments):
                for e in experiments:
                    print("- experiment_id: {}, name: {}, lifecycle_stage: {}"
                          .format(e.experiment_id, e.name, e.lifecycle_stage))

            client = MlflowClient()
            for name in ["Experiment 1", "Experiment 2"]:
                exp_id = client.create_experiment(name)

            # Delete the last experiment
            client.delete_experiment(exp_id)

            # Fetch experiments by view type
            print("Active experiments:")
            print_experiment_info(client.list_experiments(view_type=ViewType.ACTIVE_ONLY))
            print("Deleted experiments:")
            print_experiment_info(client.list_experiments(view_type=ViewType.DELETED_ONLY))
            print("All experiments:")
            print_experiment_info(client.list_experiments(view_type=ViewType.ALL))

        .. code-block:: text
            :caption: Output

            Active experiments:
            - experiment_id: 0, name: Default, lifecycle_stage: active
            - experiment_id: 1, name: Experiment 1, lifecycle_stage: active
            Deleted experiments:
            - experiment_id: 2, name: Experiment 2, lifecycle_stage: deleted
            All experiments:
            - experiment_id: 0, name: Default, lifecycle_stage: active
            - experiment_id: 1, name: Experiment 1, lifecycle_stage: active
            - experiment_id: 2, name: Experiment 2, lifecycle_stage: deleted
        """
        return self._tracking_client.list_experiments(view_type)

    def get_experiment(self, experiment_id):
        """
        Retrieve an experiment by experiment_id from the backend store

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        :return: :py:class:`mlflow.entities.Experiment`

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            client = MlflowClient()
            exp_id = client.create_experiment("Experiment")
            experiment = client.get_experiment(exp_id)

            # Show experiment info
            print("Name: {}".format(experiment.name))
            print("Experiment ID: {}".format(experiment.experiment_id))
            print("Artifact Location: {}".format(experiment.artifact_location))
            print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            Name: Experiment
            Experiment ID: 1
            Artifact Location: file:///.../mlruns/1
            Lifecycle_stage: active
        """
        return self._tracking_client.get_experiment(experiment_id)

    def get_experiment_by_name(self, name):
        """
        Retrieve an experiment by experiment name from the backend store

        :param name: The experiment name, which is case sensitive.
        :return: :py:class:`mlflow.entities.Experiment`

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Case-sensitive name
            client = MlflowClient()
            experiment = client.get_experiment_by_name("Default")

            # Show experiment info
            print("Name: {}".format(experiment.name))
            print("Experiment ID: {}".format(experiment.experiment_id))
            print("Artifact Location: {}".format(experiment.artifact_location))
            print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            Name: Default
            Experiment ID: 0
            Artifact Location: file:///.../mlruns/0
            Lifecycle_stage: active
        """
        return self._tracking_client.get_experiment_by_name(name)

    def create_experiment(self, name, artifact_location=None):
        """Create an experiment.

        :param name: The experiment name. Must be unique.
        :param artifact_location: The location to store run artifacts.
                                  If not provided, the server picks an appropriate default.
        :return: String as an integer ID of the created experiment.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create an experiment with a name that is unique and case sensitive.
            client = MlflowClient()
            experiment_id = client.create_experiment("Social NLP Experiments")
            client.set_experiment_tag(experiment_id, "nlp.framework", "Spark NLP")

            # Fetch experiment metadata information
            experiment = client.get_experiment(experiment_id)
            print("Name: {}".format(experiment.name))
            print("Experiment_id: {}".format(experiment.experiment_id))
            print("Artifact Location: {}".format(experiment.artifact_location))
            print("Tags: {}".format(experiment.tags))
            print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            Name: Social NLP Experiments
            Experiment_id: 1
            Artifact Location: file:///.../mlruns/1
            Tags: {'nlp.framework': 'Spark NLP'}
            Lifecycle_stage: active
        """
        return self._tracking_client.create_experiment(name, artifact_location)

    def delete_experiment(self, experiment_id):
        """
        Delete an experiment from the backend store.

        :param experiment_id: The experiment ID returned from ``create_experiment``.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create an experiment with a name that is unique and case sensitive
            client = MlflowClient()
            experiment_id = client.create_experiment("New Experiment")
            client.delete_experiment(experiment_id)

            # Examine the deleted experiment details.
            experiment = client.get_experiment(experiment_id)
            print("Name: {}".format(experiment.name))
            print("Artifact Location: {}".format(experiment.artifact_location))
            print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            Name: New Experiment
            Artifact Location: file:///.../mlruns/1
            Lifecycle_stage: deleted
        """
        self._tracking_client.delete_experiment(experiment_id)

    def restore_experiment(self, experiment_id):
        """
        Restore a deleted experiment unless permanently deleted.

        :param experiment_id: The experiment ID returned from ``create_experiment``.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_experiment_info(experiment):
                print("Name: {}".format(experiment.name))
                print("Experiment Id: {}".format(experiment.experiment_id))
                print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

            # Create and delete an experiment
            client = MlflowClient()
            experiment_id = client.create_experiment("New Experiment")
            client.delete_experiment(experiment_id)

            # Examine the deleted experiment details.
            experiment = client.get_experiment(experiment_id)
            print_experiment_info(experiment)
            print("--")

            # Restore the experiment and fetch its info
            client.restore_experiment(experiment_id)
            experiment = client.get_experiment(experiment_id)
            print_experiment_info(experiment)

        .. code-block:: text
            :caption: Output

            Name: New Experiment
            Experiment Id: 1
            Lifecycle_stage: deleted
            --
            Name: New Experiment
            Experiment Id: 1
            Lifecycle_stage: active
        """
        self._tracking_client.restore_experiment(experiment_id)

    def rename_experiment(self, experiment_id, new_name):
        """
        Update an experiment's name. The new name must be unique.

        :param experiment_id: The experiment ID returned from ``create_experiment``.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_experiment_info(experiment):
                print("Name: {}".format(experiment.name))
                print("Experiment_id: {}".format(experiment.experiment_id))
                print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

            # Create an experiment with a name that is unique and case sensitive
            client = MlflowClient()
            experiment_id = client.create_experiment("Social NLP Experiments")

            # Fetch experiment metadata information
            experiment = client.get_experiment(experiment_id)
            print_experiment_info(experiment)
            print("--")

            # Rename and fetch experiment metadata information
            client.rename_experiment(experiment_id, "Social Media NLP Experiments")
            experiment = client.get_experiment(experiment_id)
            print_experiment_info(experiment)

        .. code-block:: text
            :caption: Output

            Name: Social NLP Experiments
            Experiment_id: 1
            Lifecycle_stage: active
            --
            Name: Social Media NLP Experiments
            Experiment_id: 1
            Lifecycle_stage: active
        """
        self._tracking_client.rename_experiment(experiment_id, new_name)

    def log_metric(self, run_id, key, value, timestamp=None, step=None):
        """
        Log a metric against the run ID.

        :param run_id: The run id to which the metric should be logged.
        :param key: Metric name.
        :param value: Metric value (float). Note that some special values such
                      as +/- Infinity may be replaced by other values depending on the store. For
                      example, the SQLAlchemy store replaces +/- Inf with max / min float values.
        :param timestamp: Time when this metric was calculated. Defaults to the current system time.
        :param step: Integer training step (iteration) at which was the metric calculated.
                     Defaults to 0.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_run_info(r):
                print("run_id: {}".format(r.info.run_id))
                print("metrics: {}".format(r.data.metrics))
                print("status: {}".format(r.info.status))

            # Create a run under the default experiment (whose id is '0').
            # Since these are low-level CRUD operations, this method will create a run.
            # To end the run, you'll have to explicitly end it.
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            print_run_info(run)
            print("--")

            # Log the metric. Unlike mlflow.log_metric this method
            # does not start a run if one does not exist. It will log
            # the metric for the run id in the backend store.
            client.log_metric(run.info.run_id, "m", 1.5)
            client.set_terminated(run.info.run_id)
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: 95e79843cb2c463187043d9065185e24
            metrics: {}
            status: RUNNING
            --
            run_id: 95e79843cb2c463187043d9065185e24
            metrics: {'m': 1.5}
            status: FINISHED
        """
        self._tracking_client.log_metric(run_id, key, value, timestamp, step)

    def log_param(self, run_id, key, value):
        """
        Log a parameter against the run ID.

        :param run_id: The run id to which the param should be logged.
        :param value: Value is converted to a string.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_run_info(r):
                print("run_id: {}".format(r.info.run_id))
                print("params: {}".format(r.data.params))
                print("status: {}".format(r.info.status))

            # Create a run under the default experiment (whose id is '0').
            # Since these are low-level CRUD operations, this method will create a run.
            # To end the run, you'll have to explicitly end it.
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            print_run_info(run)
            print("--")

            # Log the parameter. Unlike mlflow.log_param this method
            # does not start a run if one does not exist. It will log
            # the parameter in the backend store
            client.log_param(run.info.run_id, "p", 1)
            client.set_terminated(run.info.run_id)
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: e649e49c7b504be48ee3ae33c0e76c93
            params: {}
            status: RUNNING
            --
            run_id: e649e49c7b504be48ee3ae33c0e76c93
            params: {'p': '1'}
            status: FINISHED
        """
        self._tracking_client.log_param(run_id, key, value)

    def set_experiment_tag(self, experiment_id, key, value):
        """
        Set a tag on the experiment with the specified ID. Value is converted to a string.

        :param experiment_id: String ID of the experiment.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string).

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create an experiment and set its tag
            client = MlflowClient()
            experiment_id = client.create_experiment("Social Media NLP Experiments")
            client.set_experiment_tag(experiment_id, "nlp.framework", "Spark NLP")

            # Fetch experiment metadata information
            experiment = client.get_experiment(experiment_id)
            print("Name: {}".format(experiment.name))
            print("Tags: {}".format(experiment.tags))

        .. code-block:: text
            :caption: Output

            Name: Social Media NLP Experiments
            Tags: {'nlp.framework': 'Spark NLP'}
        """
        self._tracking_client.set_experiment_tag(experiment_id, key, value)

    def set_tag(self, run_id, key, value):
        """
        Set a tag on the run with the specified ID. Value is converted to a string.

        :param run_id: String ID of the run.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string)

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_run_info(run):
                print("run_id: {}".format(run.info.run_id))
                print("Tags: {}".format(run.data.tags))

            # Create a run under the default experiment (whose id is '0').
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            print_run_info(run)
            print("--")

            # Set a tag and fetch updated run info
            client.set_tag(run.info.run_id, "nlp.framework", "Spark NLP")
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: 4f226eb5758145e9b28f78514b59a03b
            Tags: {}
            --
            run_id: 4f226eb5758145e9b28f78514b59a03b
            Tags: {'nlp.framework': 'Spark NLP'}
        """
        self._tracking_client.set_tag(run_id, key, value)

    def delete_tag(self, run_id, key):
        """
        Delete a tag from a run. This is irreversible.

        :param run_id: String ID of the run
        :param key: Name of the tag

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_run_info(run):
                print("run_id: {}".format(run.info.run_id))
                print("Tags: {}".format(run.data.tags))

            # Create a run under the default experiment (whose id is '0').
            client = MlflowClient()
            tags = {"t1": 1, "t2": 2}
            experiment_id = "0"
            run = client.create_run(experiment_id, tags=tags)
            print_run_info(run)
            print("--")

            # Delete tag and fetch updated info
            client.delete_tag(run.info.run_id, "t1")
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: b7077267a59a45d78cd9be0de4bc41f5
            Tags: {'t2': '2', 't1': '1'}
            --
            run_id: b7077267a59a45d78cd9be0de4bc41f5
            Tags: {'t2': '2'}
        """
        self._tracking_client.delete_tag(run_id, key)

    def log_batch(self, run_id, metrics=(), params=(), tags=()):
        """
        Log multiple metrics, params, and/or tags.

        :param run_id: String ID of the run
        :param metrics: If provided, List of Metric(key, value, timestamp) instances.
        :param params: If provided, List of Param(key, value) instances.
        :param tags: If provided, List of RunTag(key, value) instances.

        Raises an MlflowException if any errors occur.
        :return: None

        .. code-block:: python
            :caption: Example

            import time

            from mlflow.tracking import MlflowClient
            from mlflow.entities import Metric, Param, RunTag

            def print_run_info(r):
                print("run_id: {}".format(r.info.run_id))
                print("params: {}".format(r.data.params))
                print("metrics: {}".format(r.data.metrics))
                print("tags: {}".format(r.data.tags))
                print("status: {}".format(r.info.status))

            # Create MLflow entities and a run under the default experiment (whose id is '0').
            timestamp = int(time.time() * 1000)
            metrics = [Metric('m', 1.5, timestamp, 1)]
            params = [Param("p", 'p')]
            tags = [RunTag("t", "t")]
            experiment_id = "0"
            client = MlflowClient()
            run = client.create_run(experiment_id)

            # Log entities, terminate the run, and fetch run status
            client.log_batch(run.info.run_id, metrics=metrics, params=params, tags=tags)
            client.set_terminated(run.info.run_id)
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: ef0247fa3205410595acc0f30f620871
            params: {'p': 'p'}
            metrics: {'m': 1.5}
            tags: {'t': 't'}
            status: FINISHED
        """
        self._tracking_client.log_batch(run_id, metrics, params, tags)

    def set_terminated(self, run_id, status=None, end_time=None):
        """Set a run's status to terminated.

        :param status: A string value of :py:class:`mlflow.entities.RunStatus`.
                       Defaults to "FINISHED".
        :param end_time: If not provided, defaults to the current time.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            def print_run_info(r):
                print("run_id: {}".format(r.info.run_id))
                print("status: {}".format(r.info.status))

            # Create a run under the default experiment (whose id is '0').
            # Since this is low-level CRUD operation, this method will create a run.
            # To end the run, you'll have to explicitly terminate it.
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            print_run_info(run)
            print("--")

            # Terminate the run and fetch updated status. By default,
            # the status is set to "FINISHED". Other values you can
            # set are "KILLED", "FAILED", "RUNNING", or "SCHEDULED".
            client.set_terminated(run.info.run_id, status="KILLED")
            run = client.get_run(run.info.run_id)
            print_run_info(run)

        .. code-block:: text
            :caption: Output

            run_id: 575fb62af83f469e84806aee24945973
            status: RUNNING
            --
            run_id: 575fb62af83f469e84806aee24945973
            status: KILLED
        """
        self._tracking_client.set_terminated(run_id, status, end_time)

    def delete_run(self, run_id):
        """Deletes a run with the given ID.

        :param run_id: The unique run id to delete.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create a run under the default experiment (whose id is '0').
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            run_id = run.info.run_id
            print("run_id: {}; lifecycle_stage: {}".format(run_id, run.info.lifecycle_stage))
            print("--")
            client.delete_run(run_id)
            del_run = client.get_run(run_id)
            print("run_id: {}; lifecycle_stage: {}".format(run_id, del_run.info.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            run_id: a61c7a1851324f7094e8d5014c58c8c8; lifecycle_stage: active
            run_id: a61c7a1851324f7094e8d5014c58c8c8; lifecycle_stage: deleted
        """
        self._tracking_client.delete_run(run_id)

    def restore_run(self, run_id):
        """
        Restores a deleted run with the given ID.

        :param run_id: The unique run id to restore.

        .. code-block:: python
            :caption: Example

            from mlflow.tracking import MlflowClient

            # Create a run under the default experiment (whose id is '0').
            client = MlflowClient()
            experiment_id = "0"
            run = client.create_run(experiment_id)
            run_id = run.info.run_id
            print("run_id: {}; lifecycle_stage: {}".format(run_id, run.info.lifecycle_stage))
            client.delete_run(run_id)
            del_run = client.get_run(run_id)
            print("run_id: {}; lifecycle_stage: {}".format(run_id, del_run.info.lifecycle_stage))
            client.restore_run(run_id)
            rest_run = client.get_run(run_id)
            print("run_id: {}; lifecycle_stage: {}".format(run_id, res_run.info.lifecycle_stage))

        .. code-block:: text
            :caption: Output

            run_id: 7bc59754d7e74534a7917d62f2873ac0; lifecycle_stage: active
            run_id: 7bc59754d7e74534a7917d62f2873ac0; lifecycle_stage: deleted
            run_id: 7bc59754d7e74534a7917d62f2873ac0; lifecycle_stage: active
        """
        self._tracking_client.restore_run(run_id)

    def search_runs(
        self,
        experiment_ids,
        filter_string="",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search experiments that fit the search criteria.

        :param experiment_ids: List of experiment IDs, or a single int or string id.
        :param filter_string: Filter query string, defaults to searching all runs.
        :param run_view_type: one of enum values ACTIVE_ONLY, DELETED_ONLY, or ALL runs
                              defined in :py:class:`mlflow.entities.ViewType`.
        :param max_results: Maximum number of runs desired.
        :param order_by: List of columns to order by (e.g., "metrics.rmse"). The ``order_by`` column
                     can contain an optional ``DESC`` or ``ASC`` value. The default is ``ASC``.
                     The default ordering is to sort by ``start_time DESC``, then ``run_id``.
        :param page_token: Token specifying the next page of results. It should be obtained from
            a ``search_runs`` call.

        :return: A list of :py:class:`mlflow.entities.Run` objects that satisfy the search
            expressions. If the underlying tracking store supports pagination, the token for
            the next page may be obtained via the ``token`` attribute of the returned object.

        .. code-block:: python
            :caption: Example

            import mlflow
            from mlflow.tracking import MlflowClient
            from mlflow.entities import ViewType

            def print_run_info(runs):
                for r in runs:
                    print("run_id: {}".format(r.info.run_id))
                    print("lifecycle_stage: {}".format(r.info.lifecycle_stage))
                    print("metrics: {}".format(r.data.metrics))

                    # Exclude mlflow system tags
                    tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
                    print("tags: {}".format(tags))

            # Create an experiment and log two runs with metrics and tags under the experiment
            experiment_id = mlflow.create_experiment("Social NLP Experiments")
            with mlflow.start_run(experiment_id=experiment_id) as run:
                mlflow.log_metric("m", 1.55)
                mlflow.set_tag("s.release", "1.1.0-RC")
            with mlflow.start_run(experiment_id=experiment_id):
                mlflow.log_metric("m", 2.50)
                mlflow.set_tag("s.release", "1.2.0-GA")

            # Search all runs under experiment id and order them by
            # descending value of the metric 'm'
            client = MlflowClient()
            runs = client.search_runs(experiment_id, order_by=["metrics.m DESC"])
            print_run_info(runs)
            print("--")

            # Delete the first run
            client.delete_run(run_id=run.info.run_id)

            # Search only deleted runs under the experiment id and use a case insensitive pattern
            # in the filter_string for the tag.
            filter_string = "tags.s.release ILIKE '%rc%'"
            runs = client.search_runs(experiment_id, run_view_type=ViewType.DELETED_ONLY,
                                        filter_string=filter_string)
            print_run_info(runs)

        .. code-block:: text
            :caption: Output

            run_id: 0efb2a68833d4ee7860a964fad31cb3f
            lifecycle_stage: active
            metrics: {'m': 2.5}
            tags: {'s.release': '1.2.0-GA'}
            run_id: 7ab027fd72ee4527a5ec5eafebb923b8
            lifecycle_stage: active
            metrics: {'m': 1.55}
            tags: {'s.release': '1.1.0-RC'}
            --
            run_id: 7ab027fd72ee4527a5ec5eafebb923b8
            lifecycle_stage: deleted
            metrics: {'m': 1.55}
            tags: {'s.release': '1.1.0-RC'}
        """
        return self._tracking_client.search_runs(
            experiment_ids, filter_string, run_view_type, max_results, order_by, page_token
        )
