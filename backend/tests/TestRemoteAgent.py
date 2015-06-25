from backend.tests.TestJobManager import TestWithFakeRemoteAgent
from common.courses import Course
import time

class TestRemoteAgentOK(TestWithFakeRemoteAgent):
    def handle_job_func(self, job_id, course_id, task_id, inputdata, debug, callback_status):
        return {"result": "success", "grade": 100.0}

    def get_task_directory_hashes_func(self):
        return {"todelete": ("a random invalid hash", 3456)}

    def update_task_directory_func(self, remote_tar_file, to_delete):
        self.remote_tar_file = remote_tar_file
        self.to_delete = to_delete

    def test_job(self):
        self.job_manager.new_job(Course('test').get_task('do_run'), {"problem_1": "1"}, self.default_callback)
        result = self.wait_for_callback()
        assert "result" in result and result["result"] == "success"

    def test_update_task_directory(self):
        # give a little time to allow everything to connect, compressing the files, ...
        time.sleep(5)
        assert self.to_delete == ["todelete"]
        assert len(self.remote_tar_file) > 300