import humanize

from django.db.models import Q, F, Sum
from django.contrib.auth.models import User

from .utils import raw_sql
from .models import Submission, Question, UserData
from statistics.models import LogRecord


def get_best_users_of_week():
    SQL = """
SELECT username,
       SUM(xp) AS xp
FROM core_submission
JOIN core_question ON (core_submission.question_id = core_question.id)
RIGHT JOIN auth_user ON (core_submission.author_id=auth_user.id)
WHERE status = 'OK'
  AND core_submission.timestamp >= NOW() - '7 days'::interval
GROUP BY username
ORDER BY xp DESC
LIMIT 3;
"""
    return raw_sql(SQL)


def random_unresolved_question(user):
    questions_ok = Submission.objects.filter(author=user, status="OK").values_list(
        "question_id"
    )
    rand_question = Question.objects.exclude(
        Q(visible=False) | Q(id__in=questions_ok)
    ).order_by("?")[0]
    return rand_question


from django.conf import settings


def get_user_profile(user_id):
    user = User.objects.get(id=user_id)
    user_data = UserData(user.id, user.username)
    submissions = Submission.objects.filter(author=user).order_by("-timestamp")
    logrecords = LogRecord.objects.filter(user=user.username).order_by("-check_in")
    groups = user.groups.values_list("name", flat=True)

    # humanize.i18n.activate(
    #     "pt_BR",
    # )
    total_time_str = humanize.precisedelta(user_data.total_time_on())
    groups_str = "".join([f"{g}, " for g in groups])

    return {
        "user": user_data,
        "submissions": submissions,
        "logrecords": logrecords,
        "total_time": total_time_str,
        "groups": groups_str,
    }
