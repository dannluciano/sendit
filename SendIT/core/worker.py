from .models import Submission, CaseTest
from .submission_runner import SubmissionRunnerManager

def run_submission_runner(submission_id):
    submission = Submission.objects.get(id=submission_id)
    test_cases = CaseTest.objects.filter(questao_id=submission.question_id)
    for ct in test_cases:
        work_dir = f"{submission.id}/{ct.id}"
        submission.status = SubmissionRunnerManager().exe(
            submission.language, work_dir, ct.input, ct.output, submission.code
        )
        if submission.status != "OK":
            break
    submission.save()
    return submission.status