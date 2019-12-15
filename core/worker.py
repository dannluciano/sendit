from .models import Submission, CaseTest
from .submission_runner import SubmissionRunnerManager


def run_submission_runner(submission_id):
    submission = Submission.objects.get(id=submission_id)
    test_cases = CaseTest.objects.filter(question_id=submission.question_id)
    for ct in test_cases:
        work_dir = f"{submission.id}/{ct.id}"
        submission_result = SubmissionRunnerManager().exe(
            submission.language, work_dir, ct.sample_input, ct.sample_output, submission.code
        )
        submission.status = submission_result['status']
        submission.log = submission_result['log']
        submission.output = submission_result['output']
        submission.save()
        if submission.status != "OK":
            break
    return submission.status
