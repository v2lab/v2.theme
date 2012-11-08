# -*- coding: utf-8 -*-
# Copyright (c) 2012 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: v2_buyable_content.py 7882 2012-07-18 10:43:22Z kit $

from z3c.form import form, field
from zope import schema
from zope.annotation import IAnnotations
from zope.component import adapts
from zope.interface import Interface, implements
from Products.ATContentTypes.interfaces.document import IATDocument


class IBuyableContent(Interface):

    price = schema.TextLine(
        title=u"Price",
        description=u"Price of the content in the webshop sepatated with a comma",
        required=False)
    webshop_url = schema.TextLine(
        title=u"Webshop URL",
        description=u"URL to which the visitor should be redirected to be able to buy the content",
        required=False)


BASE_KEY = 'v2.buyable_content.'


def make_property(key, default):
    key = BASE_KEY + key

    def setter(self, value):
        self._data[key] = value
    def getter(self):
        return self._data.get(key, default)
    return property(getter, setter)


class BuyableAdapter(object):
    adapts(IATDocument)
    implements(IBuyableContent)

    def __init__(self, context):
        self.context = context
        self._data = IAnnotations(context)

    @apply
    def price():
        return make_property('price', u'')

    @apply
    def webshop_url():
        return make_property('webshop_url', u'')


class EditBuyableInformation(form.EditForm):
    fields = field.Fields(IBuyableContent)

