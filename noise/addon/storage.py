from datetime import datetime
from persistent.list import PersistentList
from zope.annotation import IAnnotations

TWITTER_KEY = "noise.addon.twitter"
FACEBOOK_KEY = "noise.addon.facebook"
EMAIL_KEY = "noise.addon.email"
HARDCOPY_KEY = "noise.addon.hardcopy"


class NoiseRecord(object):
    """ A Noise Record containing form data
    """
    _timestamp = ""
    _record = {}

    def __init__(self, timestamp, record):
        self._timestamp = timestamp
        self._record = record

    @property
    def get_record(self):
        return self._record

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
        NoiseRecord(datetime.now().strftime("%d-%m-%Y"), record)
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
