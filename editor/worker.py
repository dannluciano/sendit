import logging

from django.core.exceptions import ObjectDoesNotExist

from core.submission_runner import SubmissionRunnerManager

from .models import Runner

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def run_submission_from_editor(uuid):
    log.info(f'Runner Started {uuid}')
    try:
        runner = Runner.objects.get(uuid=uuid)
        runner_result = SubmissionRunnerManager().exe(
            runner.language, uuid, runner.input, None, runner.code
        )
        runner.output = runner_result['output']
        runner.status = runner_result['status']
        runner.log = runner_result['log']
        runner.save()
        log.info(f'Runner Endend {uuid}')
    except ObjectDoesNotExist:
        log.error(f'Runner Fail. {uuid} not Found!')
        pass
    