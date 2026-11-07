import datetime

from django import template
from django.template.defaultfilters import pluralize

register = template.Library()


def compute_machine_time(days, hours, minutes, seconds, microseconds):
    return (
        f"P{days}DT{hours}H{minutes}M{seconds}.{str(microseconds).zfill(6)}S"
    )


def compute_phrase_time(days, hours, minutes, seconds, microseconds):
    response = []
    if days:
        response.append(f"{days} dia{pluralize(days)}")
    if hours:
        response.append(f"{hours} hora{pluralize(hours)}")
    if minutes:
        response.append(f"{minutes} minuto{pluralize(minutes)}")
    if seconds:
        response_seconds = f" e {seconds} segundo{pluralize(seconds)}"

    # if microseconds:
    #     response.append(
    #         "{microseconds} microsegundo{plural_suffix}".format(
    #             microseconds=microseconds,
    #             plural_suffix=pluralize(microseconds),
    #         )
    #     )

    response = ", ".join(response)
    if seconds:
        response += response_seconds


def compute_clock_time(days, hours, minutes, seconds, microseconds):
    response = []
    if days:
        response.append(f"{days} day{pluralize(days)}")
    if hours or minutes or seconds or microseconds:
        time_string = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}"
        if seconds or microseconds:
            time_string += f":{str(seconds).zfill(2)}"
            if microseconds:
                time_string += f".{str(microseconds).zfill(6)}"

        response.append(time_string)

    response = ", ".join(response)


def compute_time_variables(remainder):
    if remainder.days > 0:
        days = remainder.days
        remainder -= datetime.timedelta(days=remainder.days)

    if round(remainder.seconds // 3600) > 1:
        hours = remainder.seconds // 3600
        remainder -= datetime.timedelta(hours=hours)

    if round(remainder.seconds // 60) > 1:
        minutes = remainder.seconds // 60
        remainder -= datetime.timedelta(minutes=minutes)

    if remainder.seconds > 0:
        seconds = remainder.seconds
        remainder -= datetime.timedelta(seconds=seconds)

    if remainder.microseconds > 0:
        microseconds = remainder.microseconds
        remainder -= datetime.timedelta(microseconds=microseconds)
    return days, hours, minutes, seconds, microseconds


@register.filter
def duration(remainder, mode=""):
    assert mode in ["machine", "phrase", "clock"]

    if not remainder:
        return ""

    days, hours, minutes, seconds, microseconds = compute_time_variables(
        remainder
    )

    modes_time = {
        "machine": compute_machine_time,
        "phrase": compute_phrase_time,
        "clock": compute_clock_time,
    }

    return modes_time[mode](days, hours, minutes, seconds, microseconds)
