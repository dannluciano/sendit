import uuid

from django.db import models


def format_time(time):
    s = time.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


class LogRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=255)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True)
    ip = models.GenericIPAddressField(unpack_ipv4=True, default="127.0.0.1")

    @property
    def duration(self):
        if self.check_out:
            return format_time(self.check_out - self.check_in)
        return "-"

    class Meta:
        ordering = ["check_in"]


class LeaderboardView(models.Model):
    SQL = """
    CREATE OR REPLACE VIEW leaderboard_view AS
    WITH DATA AS
    (SELECT auth_user.username,
          coalesce(SUM(core_question.xp) FILTER (
                                                 WHERE status='OK'), 0) AS xp,
          LEAST(coalesce(sqrt(SUM(core_question.xp) FILTER (
                                                            WHERE status='OK')) * 1.5, 0, 74))::int AS LEVEL,
        auth_group.name as group
        FROM core_submission
        JOIN core_question ON (core_submission.question_id = core_question.id)
        RIGHT JOIN auth_user ON (core_submission.author_id = auth_user.id)
        JOIN auth_user_groups ON (auth_user.id = auth_user_groups.user_id)
        JOIN auth_group ON (auth_group.id = auth_user_groups.group_id)
        GROUP BY auth_user.id, auth_group.name
        ORDER BY xp DESC)
    SELECT ROW_NUMBER() OVER () AS POSITION,
                         *
    FROM DATA;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS leaderboard_view;"""

    position = models.IntegerField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, editable=False)
    xp = models.IntegerField(editable=False)
    level = models.IntegerField(editable=False)
    group = models.CharField(max_length=255, editable=False)

    class Meta:
        managed = False
        db_table = "leaderboard_view"
        verbose_name = "Leaderboard"
        verbose_name_plural = "Leaderboard"


class StatisticsView(models.Model):
    SQL = """
    CREATE OR REPLACE VIEW statistics_view AS
    SELECT
        auth_user.username
        , coalesce(sqrt(SUM(core_question.xp) FILTER (WHERE status='OK')) * 1.5, 0)::int as level
        , coalesce(SUM(core_question.xp) FILTER (WHERE status='OK'), 0) AS xp
        , COUNT (*) FILTER (WHERE status='OK') as Number_Of_Submissions_OK
        , COUNT (*) FILTER (WHERE status <> '') as Number_Of_Submission

        , COUNT (*) FILTER (WHERE status='OK')::NUMERIC(5,2) / greatest((SELECT COUNT(*) FROM core_question), 1) * 100.0 as conclusion_rate
        , COUNT (*) FILTER (WHERE status='OK')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as sucess_rate
        , COUNT (*) FILTER (WHERE status='SintaxError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as sintax_error_rate
        , COUNT (*) FILTER (WHERE status='RuntimeError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as runtime_error_rate
        , COUNT (*) FILTER (WHERE status='TimeoutError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as timeout_error_rate
        , COUNT (*) FILTER (WHERE status='DiffError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as diff_error_rate

    FROM core_submission
    JOIN core_question ON (core_submission.question_id = core_question.id)
    RIGHT JOIN auth_user ON (core_submission.author_id = auth_user.id)
    GROUP BY auth_user.id
    ORDER BY xp DESC;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS statistics_view;"""

    username = models.CharField(primary_key=True, max_length=255, editable=False)
    level = models.IntegerField(editable=False)
    xp = models.IntegerField(editable=False)
    number_of_submissions_ok = models.IntegerField(editable=False)
    number_of_submission = models.IntegerField(editable=False)
    conclusion_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )
    sucess_rate = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    sintax_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )
    runtime_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )
    timeout_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )
    diff_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )

    class Meta:
        managed = False
        db_table = "statistics_view"
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"


class SubmissionSummaryView(models.Model):
    SQL = """
    CREATE OR REPLACE VIEW submission_summary_view AS
    SELECT core_submission.status,
        count(*) AS sum
    FROM core_submission
    GROUP BY core_submission.status 
    UNION 
    SELECT 'Total', count(*) FROM core_submission;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS submission_summary_view;"""
    status = models.CharField(primary_key=True, max_length=255, editable=False)
    sum = models.IntegerField(editable=False)

    class Meta:
        managed = False
        db_table = "submission_summary_view"
        verbose_name = "Summary of Submission"
        verbose_name_plural = "Summary of Submissions"
