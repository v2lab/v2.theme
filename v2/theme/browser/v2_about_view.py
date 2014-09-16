
from Products.CMFCore.utils import getToolByName
from collective.flowplayer.interfaces import IAudio
from collective.flowplayer.interfaces import IFlowPlayable
from v2.theme.browser.v2_people_view import V2PeopleView



class V2AboutView(V2PeopleView):
    """Complex Topic view.
    """

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
        menu_items = ['EVENT', 'PUBLISHING', 'LAB', 'WEBSHOP', 'ARCHIVE']
        for item in menu_items:
            if item in url:
                return item
