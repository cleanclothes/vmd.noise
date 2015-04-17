from Products.Five import BrowserView
from zope.interface import Interface

from ..storage import INoiseStats


class INoiseStorageView(Interface):
    """Marker interface
    """


class NoiseStorageView(BrowserView):
    def __call__(self):
        return self.render()


    def update(self):
        """
        """
        self.render()


    def render(self):
        storage = INoiseStats(self.context)

        str_form = str(self.request.form)

        noisetype = self.request.get("noisetype")
        if noisetype == "twitter":
            storage.add_twitter_noise(str_form)
        elif noisetype == "facebook":
            storage.add_facebook_noise(str_form)
        elif noisetype == "email":
            storage.add_email_noise(str_form)
        elif noisetype == "hardcopy":
            storage.add_hardcopy_noise(str_form)

        import pdb;

        pdb.set_trace()