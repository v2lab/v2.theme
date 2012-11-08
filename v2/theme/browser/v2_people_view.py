import time
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from v2.theme.browser.v2_buyable_content import IBuyableContent


class V2PeopleView(BrowserView):
    """Simple Folder view.
    """
    # XXX Rename this in V2SimpleFolderView

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def tag(self, obj, css_class='tileImage'):
        context = aq_inner(obj)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None:
            if field.get_size(context) != 0:
                scale = self.prefs.desc_scale_name
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def currenttime(self):
        return time.time()

    def trimDescription(self, desc, num=100):
        if len(desc) > num:
            res = desc[0:num]
            lastspace = res.rfind(" ")
            return res[0:lastspace] + " ..."
        return desc

    def getShoppingInformation(self, content):
        information = IBuyableContent(content, None)
        if information is not None:
            if information.price or information.webshop_url:
                # Informations are set
                detail = {}
                if information.price:
                    detail['price'] = '%.2f' % information.price
                if information.webshop_url:
                    detail['webshop_url'] = information.webshop_url
                return detail
        return None
