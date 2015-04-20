from persistent.list import PersistentList
from zope.annotation import IAnnotations

TWITTER_KEY = "noise.addon.twitter"
FACEBOOK_KEY = "noise.addon.facebook"
EMAIL_KEY = "noise.addon.email"
HARDCOPY_KEY = "noise.addon.hardcopy"


def setupAnnotations(context, key):
    annotations = IAnnotations(context)

    if not key in annotations:
        annotations[key] = PersistentList()

    return annotations


def add_noise(context, key, record):
    annotations = setupAnnotations(context, key)
    annotations[key].append(record)


def status(context, key):
    annotations = IAnnotations(context)

    return annotations.get(key, [])