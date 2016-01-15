from datetime import datetime
from persistent.list import PersistentList
from zope.annotation import IAnnotations
import logging

TWITTER_KEY = "noise.addon.twitter"
EMAIL_KEY = "noise.addon.email"
HARDCOPY_KEY = "noise.addon.hardcopy"
PETITION_KEY = "noise.addon.petition"

TWITTER_CSV_HEADERS = ["timestamp", "twitter-text", "tweet-text",
                       "firstname", "lastname", "email", "phone", "keepposted"]
EMAIL_CSV_HEADERS = ["timestamp", "email-text", "email_body", "firstname",
                     "lastname", "email", "phone", "keepposted"]
HARDCOPY_CSV_HEADERS = ["timestamp", "hardcopy-text", "hardcopy_body",
                        "firstname", "lastname", "address", "zipcode", "city",
                        "phone", "keepposted"]
PETITION_CSV_HEADERS = ["timestamp", "firstname", "lastname", "gender"]

logger = logging.getLogger('noise.addon')


class NoiseRecord(object):
    """ A Noise Record containing form data
    """

    def __init__(self, timestamp, record):
        self._timestamp = timestamp
        self._record = str(record)

    @property
    def get_record(self):
        return eval(self._record)

    @property
    def get_timestamp(self):
        return self._timestamp


def setupAnnotations(context, key, reset=False):
    annotations = IAnnotations(context)

    if reset or (not key in annotations):
        annotations[key] = PersistentList()

    return annotations


def add_noise(context, key, record):
    annotations = setupAnnotations(context, key)
    annotations[key].append(
        NoiseRecord(datetime.now().strftime("%d-%m-%Y %H:%M"), record)
    )


def get_noise(context, key):
    annotations = setupAnnotations(context, key)

    data = []
    if key in annotations:
        data = annotations[key]

    data = [d for d in data if isinstance(d, NoiseRecord)]

    return data


def status(context, key):
    annotations = IAnnotations(context)

    return annotations.get(key, [])
