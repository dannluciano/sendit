from django.db.models import Q

from .utils import raw_sql
from .models import Submission, Question


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
