from Products.CMFDefault.utils import checkEmailAddress
from five import grok
from plone.dexterity.content import Item
from plone.directives import form
from zope.annotation import IAttributeAnnotatable
from plone.namedfile.interfaces import IImageScaleTraversable

from plone import api

from .. import storage


# Interface class; used to define content-type schema.
class INoise(form.Schema, IImageScaleTraversable):
    """
    Make some noise
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/noise.xml to define the content type.

    form.model("noise.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Noise(Item):
    grok.implements(INoise, IAttributeAnnotatable)

    # Add your class methods and properties here

    @property
    def body_texts_list(self):
        return self.body_texts.split("\n")

    @property
    def total(self):
        return len(storage.status(self, storage.TWITTER_KEY)) + len(
            storage.status(self, storage.FACEBOOK_KEY)) + len(
            storage.status(self, storage.EMAIL_KEY)) + len(
            storage.status(self, storage.HARDCOPY_KEY))


# View class
# The view will automatically use a similarly named template in
# noise_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class NoiseView(grok.View):
    """ Default Noise View """

    grok.context(INoise)
    grok.require('zope2.View')

    grok.name('view')

    # Add view methods here

    def update(self):
        """ Store the request form in annotations
        """

        form = self.request.form

        noisetype = self.request.get("noisetype")

        if noisetype == "twitter":

            # Twitter form is only submitted after a succesful tweet. We
            # don't need to worry about anything else here.
            storage.add_noise(self.context, storage.TWITTER_KEY, form)

        elif noisetype == "facebook":

            storage.add_noise(self.context, storage.FACEBOOK_KEY, form)

        elif noisetype == "email":

            # E-mail sending and storage goes here

            try:

                # double check on valid email addresses
                checkEmailAddress(self.request.get("email"))
                checkEmailAddress(self.request.get("email_rcpt"))

                body = self.request.get("email_body").replace("<br/>", "\n")
                body += "\n\n{0}{1}".format(self.request.get("firstname"),
                                            self.request.get("lastname"))

                api.portal.send_email(
                    recipient=self.request.get("email_rcpt"),
                    sender="%s %s<%s>" % (
                        self.request.get("firstname"),
                        self.request.get("lastname"),
                        self.request.get("email")
                    ),
                    subject=self.request.get("email_subject"),
                    body=body,
                )

                storage.add_noise(self.context, storage.EMAIL_KEY, form)
            except:
                pass

        elif noisetype == "hardcopy":

            storage.add_noise(self.context, storage.HARDCOPY_KEY, form)

        if noisetype and self.context.thank_you_page:
            self.request.response.redirect(
                "{0}?email={1}&firstname={2}&lastname={3}".format(
                    self.context.thank_you_page, self.request.get("email"),
                    self.request.get("firstname"),
                    self.request.get("lastname")))


class NoiseStatsView(grok.View):
    """ Noise Statistics View """

    grok.context(INoise)
    grok.require('cmf.ManagePortal')

    grok.name('stats')

    @property
    def twitter_noise(self):
        return storage.get_noise(self.context, storage.TWITTER_KEY)

    @property
    def facebook_noise(self):
        return storage.get_noise(self.context, storage.FACEBOOK_KEY)

    @property
    def email_noise(self):
        return storage.get_noise(self.context, storage.EMAIL_KEY)

    @property
    def hardcopy_noise(self):
        return storage.get_noise(self.context, storage.HARDCOPY_KEY)

    def update(self):
        if self.request.get("reset") == "1":
            storage.setupAnnotations(self.context, storage.TWITTER_KEY, reset=True)
            storage.setupAnnotations(self.context, storage.FACEBOOK_KEY, reset=True)
            storage.setupAnnotations(self.context, storage.EMAIL_KEY, reset=True)
            storage.setupAnnotations(self.context, storage.HARDCOPY_KEY, reset=True)
