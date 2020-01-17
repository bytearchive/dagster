# pylint: disable-all
from dagster_graphql.implementation.pipeline_execution_manager import SubprocessExecutionManager


def mock_in_mp_process(handle, pipeline_run, instance_ref, term_event):
    return 0


class MockDagsterInstance:
    def handle_new_event(self, thing):
        pass

    def get_ref(self):
        return 1

    def get_run_by_id(self, rid):
        return rid


class MockPipeline:
    def __init__(self, name):
        self.name = name


class MockPipelineRun:
    def __init__(self, idx):
        self.run_id = idx


def test_term_event_lifecycle(mocker):
    class MockDagsterInstance:
        def handle_new_event(self, thing):
            pass

        def get_ref(self):
            return 1

        def get_run_by_id(self, rid):
            return mocker.MagicMock()

    # Mock everything except for the term event code
    instance = MockDagsterInstance()
    manager = SubprocessExecutionManager(instance)
    mocker.patch(
        'dagster_graphql.implementation.pipeline_execution_manager._in_mp_process',
        mock_in_mp_process,
    )
    mocker.patch(
        'dagster_graphql.implementation.pipeline_execution_manager.build_process_start_event'
    )
    mocker.patch('dagster_graphql.implementation.pipeline_execution_manager.gevent.spawn')
    mocker.patch('dagster_graphql.implementation.pipeline_execution_manager.check.inst_param')

    # Execute the pipeline
    assert not manager._term_events
    manager.execute_pipeline('baz', MockPipeline('foo'), MockPipelineRun(1), instance)
    assert manager._term_events
    # Ensure the pipeline run is complete so it can be collected
    mp_process = list(manager._living_process_by_run_id.values())[0]
    mp_process.join()
    # Check if collection succeeded
    manager._check_for_zombies()
    assert not manager._term_events
