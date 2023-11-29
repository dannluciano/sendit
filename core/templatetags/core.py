import datetime

from django import template
from django.template.defaultfilters import pluralize

register = template.Library()


@register.filter
def duration(value, mode=""):
    assert mode in ["machine", "phrase", "clock"]

    remainder = value
    response = ""
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    microseconds = 0

    if remainder.days > 0:
        days = remainder.days
        remainder -= datetime.timedelta(days=remainder.days)

    if round(remainder.seconds // 3600) > 1:
        hours = (remainder.seconds // 3600)
        remainder -= datetime.timedelta(hours=hours)

    if round(remainder.seconds // 60) > 1:
        minutes = (remainder.seconds // 60)
        remainder -= datetime.timedelta(minutes=minutes)

    if remainder.seconds > 0:
        seconds = remainder.seconds
        remainder -= datetime.timedelta(seconds=seconds)

    if remainder.microseconds > 0:
        microseconds = remainder.microseconds
        remainder -= datetime.timedelta(microseconds=microseconds)

    response_seconds = ""
    if mode == "machine":
        response = "P{days}DT{hours}H{minutes}M{seconds}.{microseconds}S".format(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=str(microseconds).zfill(6),
        )

    elif mode == "phrase":
        response = []
        if days:
            response.append(
                "{days} dia{plural_suffix}".format(
                    days=days,
                    plural_suffix=pluralize(days),
                )
            )
        if hours:
            response.append(
                "{hours} hora{plural_suffix}".format(
                    hours=hours,
                    plural_suffix=pluralize(hours),
                )
            )
        if minutes:
            response.append(
                "{minutes} minuto{plural_suffix}".format(
                    minutes=minutes,
                    plural_suffix=pluralize(minutes),
                )
            )
        if seconds:
            response_seconds = " e {seconds} segundo{plural_suffix}".format(
                seconds=seconds,
                plural_suffix=pluralize(seconds),
            )

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

    elif mode == "clock":
        response = []
        if days:
            response.append(
                "{days} day{plural_suffix}".format(
                    days=days,
                    plural_suffix=pluralize(days),
                )
            )
        if hours or minutes or seconds or microseconds:
            time_string = "{hours}:{minutes}".format(
                hours=str(hours).zfill(2),
                minutes=str(minutes).zfill(2),
            )
            if seconds or microseconds:
                time_string += ":{seconds}".format(
                    seconds=str(seconds).zfill(2),
                )
                if microseconds:
                    time_string += ".{microseconds}".format(
                        microseconds=str(microseconds).zfill(6),
                    )

            response.append(time_string)

        response = ", ".join(response)

    return response
