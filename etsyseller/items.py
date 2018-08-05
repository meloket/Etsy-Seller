# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtsysellerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PCAOrder = scrapy.Field()
    CustName = scrapy.Field()
    CustRef1 = scrapy.Field()
    CustRef2 = scrapy.Field()
    CustStreet = scrapy.Field()
    CustCity = scrapy.Field()
    CustState = scrapy.Field()
    CustZip = scrapy.Field()
    ShipName = scrapy.Field()
    ShipRef1 = scrapy.Field()
    ShipRef2 = scrapy.Field()
    ShipStreet = scrapy.Field()
    ShipCity = scrapy.Field()
    ShipState = scrapy.Field()
    ShipZip = scrapy.Field()
    Item = scrapy.Field()
    Qty = scrapy.Field()
    ItemDescription = scrapy.Field()
    Name = scrapy.Field()
    Item1 = scrapy.Field()
    Qty1 = scrapy.Field()
    ItemDescription1 = scrapy.Field()
    Name1 = scrapy.Field()
    Item2 = scrapy.Field()
    Qty2 = scrapy.Field()
    ItemDescription2 = scrapy.Field()
    Name2 = scrapy.Field()
    Item3 = scrapy.Field()
    Qty3 = scrapy.Field()
    ItemDescription3 = scrapy.Field()
    Name3 = scrapy.Field()
    Item4 = scrapy.Field()
    Qty4 = scrapy.Field()
    ItemDescription4 = scrapy.Field()
    Name4 = scrapy.Field()
    Item5 = scrapy.Field()
    Qty5 = scrapy.Field()
    ItemDescription5 = scrapy.Field()
    Name5 = scrapy.Field()
    Item6 = scrapy.Field()
    Qty6 = scrapy.Field()
    ItemDescription6 = scrapy.Field()
    Name6 = scrapy.Field()
    Item7 = scrapy.Field()
    Qty7 = scrapy.Field()
    ItemDescription7 = scrapy.Field()
    Name7 = scrapy.Field()
    Date = scrapy.Field()
    POBox = scrapy.Field()
    PCItemNo = scrapy.Field()
    Place = scrapy.Field()
    Phone = scrapy.Field()
    pass
