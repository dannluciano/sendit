import logging

import django_rq
from django_rq.management.commands import rqscheduler

from core.domain import compute_bests_of_week, ping

scheduler = django_rq.get_scheduler()
log = logging.getLogger(__name__)


def clear_scheduled_jobs():
    # Delete any existing jobs in the scheduler when the app starts up
    for job in scheduler.get_jobs():
        log.debug("Deleting scheduled job %s", job)
        job.delete()


def register_scheduled_jobs():
    # scheduler.cron(
    #     "0 0 * * 0",  # A cron string (e.g. "0 0 * * 0")
    #     func=compute_bests_of_week,  # Function to be queued
    #     repeat=None,  # Repeat this number of times (None means repeat forever)
    #     result_ttl=-1,  # Specify how long (in seconds) successful jobs and their results are kept. Defaults to -1 (forever)
    #     queue_name="default",  # In which queue the job should be put in
    #     use_local_timezone=False,  # Interpret hours in the local timezone
    # )
    scheduler.cron(
        '* * * * *',  # A cron string (e.g. "0 0 * * 0")
        func=ping,  # Function to be queued
        repeat=None,  # Repeat this number of times (None means repeat forever)
        result_ttl=3600,  # Specify how long (in seconds) successful jobs and their results are kept. Defaults to -1 (forever)
        queue_name="default",  # In which queue the job should be put in
        use_local_timezone=False,  # Interpret hours in the local timezone
    )


class Command(rqscheduler.Command):
    def handle(self, *args, **kwargs):
        if "now" in args:
            compute_bests_of_week()
            exit(0)
        if "ping" in args:
            ping()
            exit(0)
        clear_scheduled_jobs()
        register_scheduled_jobs()
        # from redis import Redis
        # from rq import Queue, Worker

        # redis = Redis()
        # queue = Queue(connection=redis)

        # if __name__ == '__main__':
        #     worker = Worker(queues=[queue], connection=redis)
        #     worker.work(with_scheduler=True)

        super(Command, self).handle(*args, **kwargs)
