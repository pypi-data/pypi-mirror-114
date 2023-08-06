import datetime
import pytz

EPOCH = "01/01/1970"
TZ_PARIS = "Europe/Paris"
DATE_FORMAT_DMY = "%d/%m/%Y"
DATE_FORMAT_ISO = "%Y-%m-%d %H:%M:%S"


def date_to_timestamp(stime, date_format=DATE_FORMAT_DMY, timezone=TZ_PARIS):
    timezone = pytz.timezone(timezone)
    date = datetime.datetime.strptime(stime, date_format)
    datetz = timezone.localize(date)
    return datetz.timestamp()


def timestamp_to_date(t, date_format=DATE_FORMAT_ISO):
    d = datetime.datetime.fromtimestamp(t)
    s = datetime.datetime.strftime(d, DATE_FORMAT_ISO)
    return s
