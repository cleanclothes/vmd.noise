from StringIO import StringIO
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from Products.CMFDefault.utils import checkEmailAddress
from five import grok
from plone.dexterity.content import Item
from plone.directives import form
from zope.annotation import IAttributeAnnotatable
from plone.namedfile.interfaces import IImageScaleTraversable
import logging
import csv

from plone import api

from .. import storage


logger = logging.getLogger('noise.addon')


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

    def split_lines(self, text):
        result = []
        if text:
            result = text.split("\n")
        return result

    def to_br(self, text):
        text = text.replace("\n", "<br/>")
        return text

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

                body = self.request.get("email_body").replace("<br>", "\n")
                body += "\n\n{0}\n{1} {2}".format(
                    self.context.email_conclusion,
                    self.request.get("firstname"),
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


@implementer(IPublishTraverse)
class NoiseCSVView(grok.View):
    """ Noise CSV View"""

    grok.context(INoise)
    grok.require('cmf.ManagePortal')

    grok.name('csv')

    def publishTraverse(self, request, name):
        # we have arrived, strip the stack
        request['TraversalRequestNameStack'] = []
        # return self so the publisher calls this view
        return self

    def __init__(self, context, request):
        super(NoiseCSVView, self).__init__(context, request)
        self.action, self.medium = ["", ""]
        if len(request.path) == 2:
            self.action, self.medium = request.path

    def render(self):
        if self.medium and self.action == "download":
            data = storage.get_noise(self.context,
                                     getattr(storage, "{0}_KEY".format(
                                         self.medium.upper()))
                                     )
            if data:

                out = StringIO()

                writer = csv.writer(
                    out,
                    delimiter=',',
                    quotechar='"')

                headers = getattr(storage, "{0}_CSV_HEADERS".format(
                    self.medium.upper()))

                writer.writerow(headers)

                for rec in data:
                    values = [rec.get_record.get(col) for col in headers[1:]]
                    values.insert(0, rec.get_timestamp)
                    writer.writerow(values)

                self.request.response.setHeader('Content-Type', 'text/csv')
                self.request.response.setHeader(
                    'Content-Disposition',
                    'attachment; filename="%s_data.csv"' % self.medium
                )

                return out.getvalue()


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
            storage.setupAnnotations(self.context, storage.TWITTER_KEY,
                                     reset=True)
            storage.setupAnnotations(self.context, storage.FACEBOOK_KEY,
                                     reset=True)
            storage.setupAnnotations(self.context, storage.EMAIL_KEY,
                                     reset=True)
            storage.setupAnnotations(self.context, storage.HARDCOPY_KEY,
                                     reset=True)
