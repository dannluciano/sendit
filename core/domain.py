import datetime
import logging
from statistics.models import LogRecord

import humanize
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q

from .models import Achievement, Question, Submission, UserData
from .utils import raw_sql

log = logging.getLogger(__name__)


def get_best_users_of_week():
    SQL = """
SELECT  auth_user.id,
        username,
        SUM(xp) AS xp,
        EXTRACT('week' FROM NOW()) -1 AS WEEK,
        date_trunc('week', NOW() - '1 week'::interval) AS START,
        date_trunc('week', NOW() - '0 week'::interval) AS END
FROM core_submission
JOIN core_question ON (core_submission.question_id = core_question.id)
RIGHT JOIN auth_user ON (core_submission.author_id=auth_user.id)
WHERE status = 'OK'
  AND core_submission.timestamp >= date_trunc('week', NOW() - '1 week'::interval)
  AND core_submission.timestamp <= date_trunc('week', NOW() - '0 week'::interval)
GROUP BY auth_user.id, username
ORDER BY xp DESC
LIMIT 3;
"""
    return raw_sql(SQL)


def ping():
    now = datetime.datetime.utcnow()
    log.info(f"PING {now}")
    print("--> PING", now)


def compute_bests_of_week():
    try:
        now = datetime.datetime.utcnow()
        week = now.isocalendar().week
        year = now.isocalendar().year

        log.info(f"Started Compute the Best of Week {week}")

        log.info("Creating Badge Picture")

        achievement_badge_path = (
            f"{settings.BASE_DIR}/docs/achievements/best_of_week.png"
        )
        achievement_badge_file = open(achievement_badge_path, "rb")
        achievement_badge_bytes = achievement_badge_file.read()
        achievement_badge_filename = f"Best of Week {week} - {year}"

        achievement_badge = SimpleUploadedFile(
            achievement_badge_filename,
            achievement_badge_bytes,
            content_type="image/png",
        )

        log.info("Creating Achievement")

        achievement, _ = Achievement.objects.get_or_create(
            name=achievement_badge_filename,
            defaults={
                "badge": achievement_badge,
                "xp": 10,
                "hidden": True,
            },
        )

        bests_of_week = get_best_users_of_week()
        if len(bests_of_week) > 0:
            log.info("Attaching Achievement to Users")
            bests_of_week_ids = map(
                lambda best_of_week: best_of_week.id, bests_of_week
            )
            users = User.objects.filter(id__in=bests_of_week_ids)

            achievement.users.set(users)
            achievement.save()
        else:
            log.info("No User Found")

        log.info(f"Finished Compute the Best of Week {week}")
    except Exception as err:
        log.error(err)


def random_unresolved_question(user):
    questions_ok = Submission.objects.filter(
        author=user, status="OK"
    ).values_list("question_id")
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
    submissions = Submission.objects.filter(author=user).order_by(
        "-timestamp"
    )
    logrecords = LogRecord.objects.filter(user=user.username).order_by(
        "-check_in"
    )
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
    JOIN core_achievement_users ON (
      core_achievement.id = core_achievement_users.achievement_id
    )
),
DATA AS (
  SELECT
    auth_user.username,
    coalesce(
      sum(core_question.xp) FILTER (
        WHERE
          status = 'OK'
      ),
      0
    ) + COALESCE (
      (
        SELECT
          sum(ACHIEVEMENTS.xp)
        FROM
          ACHIEVEMENTS
        WHERE
          user_id = auth_user.id
      ),
      0
    ) AS xp,
    LEAST (
      coalesce(
        sqrt(
          sum(core_question.xp) FILTER (
            WHERE
              status = 'OK'
          )
        ) * 1.5,
        0,
        74
      )
    ):: int AS LEVEL,
    auth_group.name AS GROUP,
    (
      SELECT
        array_agg(ACHIEVEMENTS.achievement_id)
      FROM
        ACHIEVEMENTS
      WHERE
        user_id = auth_user.id
    ) AS achievements
  FROM
    core_submission
    JOIN core_question ON (core_submission.question_id = core_question.id)
    RIGHT JOIN auth_user ON (core_submission.author_id = auth_user.id)
    JOIN auth_user_groups ON (auth_user.id = auth_user_groups.user_id)
    JOIN auth_group ON (auth_group.id = auth_user_groups.group_id)
  WHERE
    auth_group.name <> 'Staff'
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


def compute_leaderboard():
    leaderboard = [
        {
            "position": u.position,
            "username": u.username,
            "xp": u.xp,
            "level": u.level,
            "group": u.group,
            "achievements": u.achievements,
        }
        for u in get_leaderboard()
    ]
    return cache.get_or_set("leaderboard", leaderboard)
