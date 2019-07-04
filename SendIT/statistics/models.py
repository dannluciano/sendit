from django.db import models


class LeaderboardView(models.Model):

    SQL = """
    CREATE OR REPLACE VIEW leaderboard_view AS
    WITH DATA AS
    (SELECT auth_user.username
            , coalesce(SUM(plataforma_question.xp) FILTER (WHERE status='OK'), 0) AS xp
            , LEAST(coalesce(sqrt(SUM(plataforma_question.xp) FILTER (WHERE status='OK')) * 1.5, 0, 74))::int as level
    FROM plataforma_submission
    JOIN plataforma_question ON (plataforma_submission.questao_id = plataforma_question.id)
    RIGHT JOIN auth_user ON (plataforma_submission.autor_id = auth_user.id)
    GROUP BY auth_user.id
    ORDER BY xp DESC)
    SELECT ROW_NUMBER() OVER () as position, *
    FROM DATA;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS leaderboard_view;"""

    position = models.IntegerField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, editable=False)
    xp = models.IntegerField(editable=False)
    level = models.IntegerField(editable=False)

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
        , coalesce(sqrt(SUM(plataforma_question.xp) FILTER (WHERE status='OK')) * 1.5, 0)::int as level
        , coalesce(SUM(plataforma_question.xp) FILTER (WHERE status='OK'), 0) AS xp
        , COUNT (*) FILTER (WHERE status='OK') as Number_Of_Submissions_OK
        , COUNT (*) FILTER (WHERE status <> '') as Number_Of_Submission

        , COUNT (*) FILTER (WHERE status='OK')::NUMERIC(5,2) / greatest((SELECT COUNT(*) FROM plataforma_question), 1) * 100.0 as conclusion_rate
        , COUNT (*) FILTER (WHERE status='OK')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as sucess_rate
        , COUNT (*) FILTER (WHERE status='SintaxError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as sintax_error_rate
        , COUNT (*) FILTER (WHERE status='RuntimeError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as runtime_error_rate
        , COUNT (*) FILTER (WHERE status='TimeoutError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as timeout_error_rate
        , COUNT (*) FILTER (WHERE status='DiffError')::NUMERIC(5,2) / greatest(COUNT (*), 1) * 100.0 as diff_error_rate

    FROM plataforma_submission
    JOIN plataforma_question ON (plataforma_submission.questao_id = plataforma_question.id)
    RIGHT JOIN auth_user ON (plataforma_submission.autor_id = auth_user.id)
    GROUP BY auth_user.id
    ORDER BY xp DESC;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS statistics_view;"""

    username = models.CharField(
        primary_key=True, max_length=255, editable=False)
    level = models.IntegerField(editable=False)
    xp = models.IntegerField(editable=False)
    number_of_submissions_ok = models.IntegerField(editable=False)
    number_of_submission = models.IntegerField(editable=False)
    conclusion_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)
    sucess_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)
    sintax_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)
    runtime_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)
    timeout_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)
    diff_error_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False)

    class Meta:
        managed = False
        db_table = "statistics_view"
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"


class SubmissionSummaryView(models.Model):
    SQL = """
    CREATE OR REPLACE VIEW submission_summary_view AS
    SELECT plataforma_submission.status,
        count(*) AS sum
    FROM plataforma_submission
    GROUP BY plataforma_submission.status 
    UNION 
    SELECT 'Total', count(*) FROM plataforma_submission;
    """

    REVERSE_SQL = """DROP VIEW IF EXISTS submission_summary_view;"""
    status = models.CharField(primary_key=True, max_length=255, editable=False)
    sum = models.IntegerField(editable=False)

    class Meta:
        managed = False
        db_table = "submission_summary_view"
        verbose_name = "Summary of Submission"
        verbose_name_plural = "Summary of Submissions"
