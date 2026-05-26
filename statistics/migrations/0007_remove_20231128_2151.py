from statistics.models import LeaderboardView, StatisticsView, SubmissionSummaryView

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("statistics", "0006_auto_20200711_1925"),
    ]

    operations = [
        migrations.RunSQL(LeaderboardView.REVERSE_SQL, LeaderboardView.SQL),
        migrations.RunSQL(StatisticsView.REVERSE_SQL, StatisticsView.SQL),
        migrations.RunSQL(SubmissionSummaryView.REVERSE_SQL, SubmissionSummaryView.SQL),
    ]
