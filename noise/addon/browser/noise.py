from Products.Five import BrowserView
from zope.interface import Interface


class INoiseView(Interface):
    """Marker interface
    """


class NoiseView(BrowserView):
    """
    """
