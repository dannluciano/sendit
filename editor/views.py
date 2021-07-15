import django_rq
import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .worker import run_submission_from_editor
from .models import Runner

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

@login_required
def editor(request):
    return render(request, 'editor/editor.html')

@login_required
@require_POST
def create_runner(request):
    log.info("New Runner from Editor")
    data = json.loads(request.body.decode("utf-8"))
    runner = Runner.objects.create(
        code=data['code'], 
        language=data['lang'],
        input=data['input']
    )
    ttl = 60*60*24*7
    django_rq.enqueue(run_submission_from_editor, runner.uuid, ttl=ttl, result_ttl=ttl)
    log.info("Runner was to Queue")
    return JsonResponse({
        'status': 'ok',
        'uuid': runner.uuid,
    })

def runner_details(request, runner_uuid):
    try:
        runner = Runner.objects.get(uuid=runner_uuid)
        return JsonResponse(model_to_dict(runner, fields=['status','output']))
    except ObjectDoesNotExist:
        return JsonResponse({'msg': 'Not Found'}, status=404)