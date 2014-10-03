import time
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from v2.theme.browser.v2_buyable_content import IBuyableContent
from Products.CMFCore.utils import getToolByName
from collective.flowplayer.interfaces import IAudio
from collective.flowplayer.interfaces import IFlowPlayable
import feedparser
import HTMLParser

v2_vimeo_rss_url = "http://vimeo.com/channels/349409/videos/rss"


class V2GenericView(BrowserView):
    """Simple Folder view.
    """

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
                    detail['price'] = information.price
                if information.webshop_url:
                    detail['webshop_url'] = information.webshop_url
                return detail
        return None

    def getCategoryByURL(self, url):
        """Find the parent name in the url path.

        This displays in which category an item is placed."""

        url_low = url.lower()
        menu_items = ['event','events', 'publishing', 'lab','about','organization','webshop','shop','archive']
        for item in menu_items:
            if item in url_low:
                return item
        return "v2"

    def toLocalizedTime(self, time, long_format=None, time_only = None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        try:
            return util.ulocalized_time(time, long_format, time_only, self.context,
                                        domain='plonelocales')
        except TypeError: # Plone 3.1 has no time_only argument
            return util.ulocalized_time(time, long_format, self.context,
                                        domain='plonelocales')

    def getSubFolderContents(self, folder):
        catalog = getToolByName(self, 'portal_catalog')
        if folder.portal_type == "Folder":
            path = folder.getPath()
            return catalog.searchResults(
                path={'query': path, 'depth': 1},
                sort_on='getObjPositionInParent', sort_limit=3)[:3]
        if folder.portal_type == "Topic":
            query = folder.getObject().buildQuery()
            if query is not None:
                return catalog.searchResults(query)[:3]
        return []

    def isVideo(self, content):
        if IFlowPlayable.providedBy(content):
            return True
        extension = content.id[-3:]
        return (extension == "mov" or
                extension == "avi" or
                extension == "mp4" or
                extension == "m4v")

    def isAudio(self, content):
        return IAudio.providedBy(content)

    def getCategory(self, content):
        """Find the parent name in the url path.

        This displays in which category an item is placed."""

        url = content.virtual_url_path().upper()
        menu_items = ['EVENT', 'PUBLISHING', 'LAB']
        for item in menu_items:
            if item in url:
                return item

    def getVideos(self):
        # h = HTMLParser.HTMLParser()
        # videos = []
        # for entry in feed.entries:
        #     videos.append( h.unescape(entry.summary) )
        feed = feedparser.parse( v2_vimeo_rss_url )

        videos = []
        for entry in feed.entries:
            video =[]
            # video.append( entry.links[0]["href"].split('/349409/')[1] )
            video.append( entry.link )
            video.append( entry.summary.split('img src="')[1].split('_200x150.jpg')[0] )
            video.append( entry.title )
            videos.append( video )
        return videos

    def getVideo(self, content):
        # entries = []
        # entries.extend( feed[ "items" ] )
        # sorted_entries = sorted(entries, key=lambda entry: entry["date_parsed"])
        # sorted_entries.reverse() # for most recent entries first
        # return sorted_entries[0].links[0]["href"].split('/349409/')[1]
        feed = feedparser.parse( v2_vimeo_rss_url )

        return feed.entries[0].links[0]["href"].split('/349409/')[1]