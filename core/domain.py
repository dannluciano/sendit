from statistics.models import LogRecord

import humanize
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Question, Submission, UserData
from .utils import raw_sql


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
    rand_questions = Question.objects.exclude(
        Q(visible=False) | Q(id__in=questions_ok)
    ).order_by("?")
    if rand_questions:
        return rand_questions[0]
    else:
        return None


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

def get_leaderboard():
    SQL = """
WITH ACHIEVEMENTS AS (
	SELECT
		*
	FROM
		core_achievement
		JOIN core_achievement_users ON (core_achievement.id = core_achievement_users.achievement_id)
),
DATA AS (
	SELECT
		auth_user.username,
		coalesce(sum(core_question.xp) FILTER (WHERE status = 'OK') + (
				SELECT
					sum(ACHIEVEMENTS.xp)
				FROM ACHIEVEMENTS
				WHERE
					user_id = auth_user.id), 0) AS xp,
	LEAST (coalesce(sqrt(sum(core_question.xp) FILTER (WHERE status = 'OK')) * 1.5, 0, 74))::int AS LEVEL,
	auth_group.name AS
GROUP,
(
	SELECT
		array_agg(ACHIEVEMENTS.achievement_id)
	FROM
		ACHIEVEMENTS
	WHERE
		user_id = auth_user.id) AS achievements
FROM
	core_submission
	JOIN core_question ON (core_submission.question_id = core_question.id)
		RIGHT JOIN auth_user ON (core_submission.author_id = auth_user.id)
		JOIN auth_user_groups ON (auth_user.id = auth_user_groups.user_id)
		JOIN auth_group ON (auth_group.id = auth_user_groups.group_id)
	GROUP BY
		auth_user.id,
		auth_group.name
	ORDER BY
		xp DESC
)
SELECT
	row_number() OVER () AS POSITION,
	*
FROM
	DATA;
        """
    return raw_sql(SQL)