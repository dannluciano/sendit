from .models import Submission, CaseTest
from .submission_runner import SubmissionRunnerManager


def run_submission_runner(submission_id):
    submission = Submission.objects.get(id=submission_id)
    test_cases = CaseTest.objects.filter(question_id=submission.question_id)
    last_status = submission.status
    last_log = ''
    last_output = ''
    for ct in test_cases:
        work_dir = f"{submission.id}/{ct.id}"
        submission_result = SubmissionRunnerManager().exe(
            submission.language, work_dir, ct.sample_input, ct.sample_output, submission.code
        )
        last_status = submission_result['status']
        last_log = submission_result['log']
        last_output = submission_result['output']
        if last_status != "OK":
            break
    submission.status = last_status
    submission.log = last_log
    submission.output = last_output
    submission.save()
    return submission.status
