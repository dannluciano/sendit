from .models import Submission, CaseTest
from .submission_runner import SubmissionRunnerManager

def run_submission_runner(submission_id):
    submission = Submission.objects.get(id=submission_id)
    casos_de_testes = CaseTest.objects.filter(questao_id=submission.questao_id)
    for ct in casos_de_testes:
        work_dir = f"{submission.id}/{ct.id}"
        submission.status = SubmissionRunnerManager().exe(
            submission.language, work_dir, ct.entrada, ct.saida, submission.codigo
        )
        if submission.status != "OK":
            break
    submission.save()
    return submission.status