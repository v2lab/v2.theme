from Products.Five import BrowserView

from collective.contentleadimage.config import IMAGE_FIELD_NAME

class SocialTagsView(BrowserView):
    """Social media tag for the leadImage."""

    @property
    def image(self):
        default_image = 'http://v2.nl/logo.png'

        if hasattr(self.context, 'getField'):
            # Copied from collective.contentleadimage.utils:hasContentLeadImage
            field = self.context.getField(IMAGE_FIELD_NAME)
            if field is not None:
                value = field.get(self.context)
                if not not value:
                    url = self.context.absolute_url() +'/'
                    return url + field.getScaleName('large')
        return default_image
