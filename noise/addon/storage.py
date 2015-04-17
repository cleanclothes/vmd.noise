import zope
from zope.interface import implements
from zope.annotation import factory
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from noise.addon.models.noise import INoise

KEY = "noise.addon.stats"


class INoiseStats(Interface):
    """
    """

    def add_twitter_noise(self):
        """
        """

    def add_facebook_noise(self):
        """
        """

    def add_email_noise(self):
        """
        """

    def add_hardcopy_noise(self):
        """
        """

    def status(self):
        """
        """


class NoiseStats(object):
    implements(INoiseStats)
    zope.component.adapts(INoise)

    def add_twitter_noise(self, record):
        if not hasattr(self,"_twitter_noise"):
            self._twitter_noise = set()
        self._twitter_noise.add(record)

    def add_facebook_noise(self, record):
        self._facebook_noise.add(record)

    def add_email_noise(self, record):
        self._email_noise.add(record)

    def add_hardcopy_noise(self, record):
        self._hardcopy_noise.add(record)

    def status(self):
        return [
            len(self._twitter_noise),
            len(self._facebook_noise),
            len(self._email_noise),
            len(self._hardcopy_noise)
        ]

# Register as adapter (you may do this in ZCML too)
zope.component.provideAdapter(factory(NoiseStats, key=KEY))
