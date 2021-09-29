import uuid
import django_rq
import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse

from .worker import run_submission_from_editor
from .models import FileCode, Runner

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
    django_rq.enqueue(run_submission_from_editor,
                      runner.uuid, ttl=ttl, result_ttl=ttl)
    log.info("Runner was to Queue")
    return JsonResponse({
        'status': 'ok',
        'uuid': runner.uuid,
    })


@login_required
def runner_details(request, runner_uuid):
    try:
        runner = Runner.objects.get(uuid=runner_uuid)
        return JsonResponse(model_to_dict(runner, fields=['status', 'output']))
    except ObjectDoesNotExist:
        return JsonResponse({'msg': 'Not Found'}, status=404)


@login_required
@require_POST
def file_code_save(request):
    log.info("File Code Save")
    try:
        owner = request.user
        name = request.POST['filename']
        code = request.POST['filesrc']
        language = request.POST['language']

        file_code_dict = {
            'code': code,
            'language': language,
        }

        file_code, created = FileCode.objects.update_or_create(
            name=name,
            owner=owner,
            defaults=file_code_dict
        )

        return JsonResponse({
            'status': 'ok',
            'uuid': file_code.uuid,
            'created': created
        })
    except Exception as e:
        return JsonResponse({
            'error': e.__class__.__name__,
            'msg': str(e)
        })


@login_required
def file_code_list(request):
    owner = request.user
    filecodes = FileCode.objects.filter(owner=owner).order_by('-updated_at')
    return render(request, 'editor/files.html', context={
        'filecodes': filecodes
    })


@login_required
def file_code_detail(request, file_code_uuid):
    file_code = get_object_or_404(FileCode, uuid=file_code_uuid)
    return render(request, 'editor/editor.html', context={
        'last_submission': file_code
    })


@login_required
@require_POST
def file_code_destroy(request, file_code_uuid):
    file_code = get_object_or_404(FileCode, uuid=file_code_uuid)
    file_code.delete()
    return redirect(reverse('editor:file-code-list'))
