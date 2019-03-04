# -*- coding: utf-8 -*-
import scrapy
from etsyseller.items import EtsysellerItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from scrapy.http import TextResponse
from lxml import html
from lxml import etree
import csv
import unicodedata
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import re
import Tkinter
import tkMessageBox


class DictUnicodeProxy(object):
    def __init__(self, d):
        self.d = d
    def __iter__(self):
        return self.d.__iter__()
    def get(self, item, default=None):
        i = self.d.get(item, default)
        if isinstance(i, unicode):
            return i.encode('utf-8')
        return i

class ExmlparserSpider(scrapy.Spider):
    name = 'exmlparser'
    
    def __init__(self):
        chrome_driver = "etsyseller/chromedriver/chromedriver.exe"
        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary
        # self.driver = webdriver.Chrome(chrome_driver, chrome_options = options)
        self.driver = webdriver.Chrome(chrome_driver)
        # init_url = ['https://www.etsy.com/your/orders/sold?ref=seller-platform-mcnav']
        # # self.start_urls = ['http://localhost/emulatedurl/etsyall.html']

        # # init_url = 'http://sellercentral.amazon.com'
        # # init_url = 'http://localhost/emulatedurl/manage.html'
        # self.driver.get(init_url)
        # response0 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        # self.parse(response0)





    # def __init__(self):

    #     chrome_driver = "etsyseller/chromedriver/chromedriver.exe"
    #     self.driver = webdriver.Chrome(chrome_driver)


    def start_requests(self):
        init_url = 'https://www.etsy.com/your/orders/sold?ref=seller-platform-mcnav'
        # init_url = 'http://localhost/emulatedurl/etsyall.html'
        self.driver.get(init_url)
        response0 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        self.parse(response0)







    def parse(self, response):

        self.driver.get(response.url)

        
        
        # # # # *************** Log in ********************************
        
        try:
            self.driver.find_element_by_id('join_neu_email_field').send_keys('afsd@gadg.com')
            self.driver.find_element_by_id("join_neu_password_field").send_keys('agegge')
            self.driver.find_element_by_xpath('.//*[contains(@class, "checkbox")]').click()
            self.driver.find_element_by_name('submit_attempt').click()
            
        except Exception as e:
            self.driver.find_element_by_id('username-existing').send_keys('sales@americanpersonalizedproducts.com')
            self.driver.find_element_by_id("password-existing").send_keys('328Sawmill')
            self.driver.find_element_by_xpath('.//*[contains(@class, "checkbox")]').click()
            self.driver.find_element_by_id('signin_button').click()
        time.sleep(30)
        (self.driver.find_elements_by_xpath("//label[contains(@class, 'radio-custom mb-xs-1')]/span[contains(@class, 'radio-label pl-xs-1')]"))[4].click()
        time.sleep(10)

        print("-------------------------------start------------------------\n")
        self.parseItem()
        # for item in items:
        #     print("\nTitle : "+item["Title"]+"\n")
        print(" -------------------------------end-------------------------\n")
        self.driver.close()

        tkMessageBox.showinfo("Result", "End!")
        pass


    def parseItem(self):
        items = []
        #each trip div has desribed two trip legs, we have to create 2 elements for each div
        with open('result/data.csv', 'wb') as csvfile:
            fieldnames = ["PCAOrder", "CustName", "CustRef1", "CustRef2", "CustStreet", "CustCity", "CustState", "CustZip", "ShipName", "ShipRef1", "ShipRef2", "ShipStreet", "ShipCity", "ShipState", "ShipZip", "Item", "Qty", "ItemDescription", "Name", "Item1", "Qty1", "ItemDescription1", "Name1", "Item2", "Qty2", "ItemDescription2", "Name2", "Item3", "Qty3" ,"ItemDescription3", "Name3", "Item4", "Qty4", "ItemDescription4", "Name4", "Item5", "Qty5", "ItemDescription5", "Name5", "Item6", "Qty6", "ItemDescription6", "Name6", "Item7", "Qty7", "ItemDescription7", "Name7", "Date", "POBox", "PCItemNo", "Place", "Phone"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            sIndex = 0

            ASINArray = self.driver.find_elements_by_xpath("//span[contains(@class, 'mr-xs-1')][1]/a[contains(@class, 'text-gray')]")
            for arrayitem in ASINArray:
                tempasincode = arrayitem.text.replace("#", "")
                print("ASIN:   AAAAAAAA:  " + tempasincode)
                
                print("ASIN:   BBBBBBBBBBB:  " + self.driver.find_elements_by_xpath("//span[contains(@class, 'mr-xs-1')][1]/a[contains(@class, 'text-gray')]")[0].text)
            
            print("COUNT:  " + str(ASINArray.__len__()) + "\n")
            # for x in range(0, ASINArray.__len__()):
            #     aaa = str((self.driver.find_elements_by_xpath("//div[contains(@class, 'orders-full-width-panel-on-mobile panel panel-no-footer mb-xs-4')]"))[x].text)
            #     print("HHHHHHHHHHHH:  " + str(x) + "\n" + aaa)


            for x in range(0, ASINArray.__len__()):
                
                time.sleep(5)

                (self.driver.find_elements_by_xpath("//div[contains(@class, 'flag')]/div[contains(@class, 'flag-body pt-xs-3 pt-xl-4 pr-xs-3 pr-md-0')]"))[x].click()
                print("HHHHHHHHHHHHHH: INDEX:  " + str(x) + "\n")
                print("HHHHHHHHHHHHHH:  CONTENT:  " + (self.driver.find_elements_by_xpath("//div[contains(@class, 'flag')]/div[contains(@class, 'flag-body pt-xs-3 pt-xl-4 pr-xs-3 pr-md-0')]"))[x].text)

                # self.driver.get("http://localhost/emulatedurl/etsydetail.html")
                subcontent = self.driver.find_elements_by_xpath("//div[contains(@class, 'overflow-y-scroll height-full')]/div")[0]
                item = EtsysellerItem()
                print("SubContent: " + str(subcontent.text))

                time.sleep(5)
                
                # d_order = ASINArray[x].text
                try:
                    d_order = str(subcontent.find_elements_by_xpath("//span[contains(@class, 'display-inline-block')]/a[1]")[0].text)
                    # print("OOOOOOOOOOO: "+d_order)
                    pass
                except Exception as e:
                    d_order = ""
                    pass
                
                try:
                    d_custname = subcontent.find_elements_by_xpath("//span[contains(@class, 'name')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custname = ""
                    pass
                
                try:
                    d_custref1 = subcontent.find_elements_by_xpath("//span[contains(@class, 'first-line')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custref1 = ""
                    pass

                try:
                    d_custref2 = subcontent.find_elements_by_xpath("//span[contains(@class, 'second-line')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custref2 = ""
                    pass

                try:
                    d_custcity = subcontent.find_elements_by_xpath("//span[contains(@class, 'city')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custcity = ""
                    pass

                try:
                    d_custstate = subcontent.find_elements_by_xpath("//span[contains(@class, 'state')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custstate = ""
                    pass

                try:
                    d_custzip = subcontent.find_elements_by_xpath("//span[contains(@class, 'zip')]")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_custzip = ""
                    pass

                try:
                    d_sku_item = subcontent.find_elements_by_xpath("//span/p/span")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_sku_item = ""
                    pass

                try:
                    d_qty = subcontent.find_elements_by_xpath("//div[contains(@class, 'col-group pl-xs-0 pt-xs-3 pr-xs-0 pb-xs-3 bb-xs-1')]/div[contains(@class, 'col-xs-2 pl-xs-0 text-center')]/p")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_qty = ""
                    pass

                try:
                    d_itemdesc = subcontent.find_elements_by_xpath("//pre/span")[0].text
                    itemdescarray = d_itemdesc.split(":")
                    if len(itemdescarray) != 0:
                        d_itemdesc = itemdescarray[-1].strip()
                    # print("DDDDDDDDDDD: "+d_custname)
                    pass
                except Exception as e:
                    d_itemdesc = ""
                    pass

                try:
                    d_orderDate = subcontent.find_elements_by_xpath("//div[contains(@class, 'flag-img flag-img-right no-wrap text-right vertical-align-bottom hide-xs hide-sm')]/div[contains(@class, 'text-body-smaller mt-xs-1')]")[0].text
                    orderDateArray = d_orderDate.split(",")
                    d_orderDate = orderDateArray[1].strip() + "," + orderDateArray[2] + "," + orderDateArray[3]

                    cstrdate = datetime.strptime(d_orderDate, '%a, %b %d, %Y')
                    d_orderDate = datetime.strftime(cstrdate, '%m/%d/%Y')
                    pass
                except Exception as e:
                    d_orderDate = ""
                    pass

                try:
                    d_place = subcontent.find_elements_by_xpath("//div[contains(@class, 'strong text-body-smaller')]/span")[0].text
                    # print("DDDDDDDDDDD: "+d_custname)//div[contains(@class, 'strong text-body-smaller')]/span
                    pass
                except Exception as e:
                    d_place = ""
                    pass

                print("RRRRRRRRRRRR:   PCAOrder: " + d_order + "   CustName:  " + d_custname + "   CustRef1:  " + d_custref1 + "   CustRef2:  " + d_custref2 + "   Custcity:  " + d_custcity + "   Custstate:  " + d_custstate + "   Custzip:  " + d_custzip + "   SKU:  " + d_sku_item + "   QTY:  " + d_qty + "   ItemDescription:  " + d_itemdesc + "   Place:  " + d_place + "   EEEEEEEEEEEEECCCCCCCCCCCCCCCCCGGGGGGGGGGGHHHHHHH")

                time.sleep(1)
                item['PCAOrder'] = d_order
                item['CustName'] = d_custname
                item['CustRef1'] = d_custref1
                item['CustRef2'] = d_custref2
                item['CustStreet'] = ""
                item['CustCity'] = d_custcity
                item['CustState'] = d_custstate
                item['CustZip'] = d_custzip
                item['ShipName'] = d_custname
                item['ShipRef1'] = d_custref1
                item['ShipRef2'] = d_custref2
                item['ShipStreet'] = ""
                item['ShipCity'] = d_custcity
                item['ShipState'] = d_custstate
                item['ShipZip'] = d_custzip
                item['Item'] = d_sku_item
                item['Qty'] = d_qty
                item['ItemDescription'] = d_itemdesc
                item['Name'] = d_itemdesc
                item['Item1'] = ""
                item['Qty1'] = ""
                item['ItemDescription1'] = ""
                item['Name1'] = ""
                item['Item2'] = ""
                item['Qty2'] = ""
                item['ItemDescription2'] = ""
                item['Name2'] = ""
                item['Item3'] = ""
                item['Qty3'] = ""
                item['ItemDescription3'] = ""
                item['Name3'] = ""
                item['Item4'] = ""
                item['Qty4'] = ""
                item['ItemDescription4'] = ""
                item['Name4'] = ""
                item['Item5'] = ""
                item['Qty5'] = ""
                item['ItemDescription5'] = ""
                item['Name5'] = ""
                item['Item6'] = ""
                item['Qty6'] = ""
                item['ItemDescription6'] = ""
                item['Name6'] = ""
                item['Item7'] = ""
                item['Qty7'] = ""
                item['ItemDescription7'] = ""
                item['Name7'] = ""
                item['Date'] = d_orderDate
                item['POBox'] = ""
                item['PCItemNo'] = ""
                item['Place'] = d_place
                item['Phone'] = ""

                # self.driver.back()
                writer.writerow(DictUnicodeProxy(item))

                self.driver.find_element_by_xpath("//button[contains(@class, 'btn btn-transparent text-white p-xs-1 mt-xs-3 mr-xs-1 icon-b-2 position-absolute position-outside-left position-top animated animated-fade-in')]").click()
                time.sleep(15)
            csvfile.close()

        self.driver.find_element_by_xpath("//button[contains(@class, 'account-button unstyled-button text-decoration-none pl-xs-3 pt-xs-2 pb-xs-2 bt-xs-1 pr-xs-3')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//ul[contains(@class, 'list-nav pt-xs-2')]/li[3]/a[contains(@class, 'list-nav-item')]").click()
        time.sleep(5)
        # return items












        # class XmlparserSpider(scrapy.Spider):
        #     name = 'xmlparser'
        #     domain = ''
        #     hflag = 'no'
        #     items = []
        #     # allowed_urls = ['https://www.sellercentral.amazon.com']
        #     # start_urls = ['https://www.amazon.com/products/dress']

        #     custom_settings = {
        #         # specifies exported fields and order
        #         'FEED_EXPORT_FIELDS': ["OrderID", "Ship Name", "Ship Street", "Ship City", "Ship State", "Ship ZipCode", "Ship OrderDate", "SKU", "Personalization", "Repersonalization"],
        #     }

        #     current_orderID = ''
        #     current_address_ship_name = ''
        #     current_address_ship_street = ''
        #     current_address_ship_city = ''
        #     current_address_ship_state = ''
        #     current_address_ship_zipcode = ''
        #     current_orderDate = ''
        #     current_sku = ''
        #     current_personalization = ''
        #     current_repersonalization = ''




        #     def __init__(self):

        #         # script_dir = os.path.dirname(__file__)
        #         # chrome_options = Options()
        #         # chrome_options.add_argument("--headless")
        #         # chrome_options.add_argument("--window-size=1920x1080")
        #         # self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        #         # self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        #         with open('C:\CSV\APP\data.csv', 'wb') as csvfile:
        #             fieldnames = ["PCAOrder", "CustName", "CustRef1", "CustRef2", "CustStreet", "CustCity", "CustState", "CustZip", "ShipName", "ShipRef1", "ShipRef2", "ShipStreet", "ShipCity", "ShipState", "ShipZip", "Item", "Qty", "ItemDescription", "Name", "Item1", "Qty1", "ItemDescription1", "Name1", "Item2", "Qty2", "ItemDescription2", "Name2", "Item3", "Qty3" ,"ItemDescription3", "Name3", "Item4", "Qty4", "ItemDescription4", "Name4", "Item5", "Qty5", "ItemDescription5", "Name5", "Item6", "Qty6", "ItemDescription6", "Name6", "Item7", "Qty7", "ItemDescription7", "Name7", "Date", "POBox", "PCItemNo", "Place", "Phone"]
        #             # fieldnames = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"]
        #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        #             writer.writeheader()
        #             csvfile.close()

        #         chrome_driver = "amazonseller/chromedriver/chromedriver.exe"
        #         self.driver = webdriver.Chrome(chrome_driver)


        #     def start_requests(self):
        #         init_url = 'http://sellercentral.amazon.com'
        #         # init_url = 'http://localhost/emulatedurl/manage.html'
        #         self.driver.get(init_url)
        #         response0 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        #         self.parse(response0)
        #         # yield scrapy.Request(url=self.driver.current_url, callback=self.body)


        #     def parse(self, response):
                
        #         self.driver.find_element_by_id('sign-in-button').click()
                
        #         # # # # *************** Log in ********************************
                
        #         self.driver.find_element_by_id('ap_email').send_keys('orders@americanpersonalizedproducts.com')
        #         self.driver.find_element_by_id("ap_password").send_keys('328Sawmill')
        #         form = self.driver.find_element_by_name("signIn")
        #         form.submit()
        #         time.sleep(90)

        #         # # *************** Goto Manage Order Page  ***************
        #         self.driver.get("https://sellercentral.amazon.com/gp/orders-v2/list/ref=ag_myo_dnav_xx_")
        #         # # self.driver.get('http://localhost/emulatedurl/manage.html')


        #         # # ***************** Last 3 Days Select and Click Search Button ******************
        #         select_3dy = Select(self.driver.find_element_by_id('_myoLO_preSelectedRangeSelect'))
        #         select_3dy.select_by_visible_text('Last 3 days')
        #         self.driver.find_element_by_id('SearchID').click()
        #         time.sleep(5)

        #         # # ***************** Set 50 Show and Click Go Button ******************
        #         select_50go = Select(self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr/td/form/table/tbody/tr/td[2]/select'))
        #         select_50go.select_by_visible_text('50')
        #         form_show = self.driver.find_element_by_xpath("//form[contains(@class, 'myo_list_orders_search_form')]")
        #         form_show.submit()
        #         time.sleep(5)


        #         # source = self.driver.page_source.encode("utf8")
        #         # maintree = etree.HTML(source)
        #         # print(str(maintree))

        #         response2 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')



        #         # # ***************** Get Printing Page Request URL *******************
        #         printing_url = "https://sellercentral.amazon.com/orders/packing-slip/ref=ag_bulkslip_cont_myo?orderIds="
        #         orderIDs = response2.xpath('//div[@id="myo-table"]/table/tbody/tr/td/a/strong/text()').extract()

        #         for orderID in orderIDs:
        #             printing_url += orderID +";"
        #             print("\n " + orderID)
                
        #         print("\n SSSSSSSSSSSSSS:   " + printing_url + "\n")

        #         #***************** Get Printing Page ******************************
        #         # printing_url = "http://localhost/emulatedurl/amazon5.html"




        #         self.driver.get(printing_url)

        #         response1 = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        #         self.get_page_block(response1)
        #         # yield scrapy.Request(url=printing_url, callback=self.get_page_block)




        #         # # # ***************** Select Print packing slip item and CheckBox then Click Go Button ******************
        #         # select_print_slip = Select(self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[2]/td/select'))
        #         # select_print_slip.select_by_visible_text('Print packing slips for selected orders')
        #         # self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[3]/td[1]/input[contains(@class, "checkall")]').click()
        #         # self.driver.find_element_by_xpath('//div[@id="myo-table"]/table/tbody/tr[2]/td/span[contains(@class, "action-go")]').click()
        #         # time.sleep(1)

        #         # source = self.driver.page_source.encode("utf8")
        #         # tree = etree.HTML(source)

        #         # print(str(source))

        #         # blocks = tree.xpath('//table/tbody//tr')


        #         # source = self.driver.page_source.encode("utf8")
        #         # tree = etree.HTML(source)
        #         # store_list = tree.xpath('//section//div[contains(@class, "stores")]//a[2]/@href')
        #         # for store in store_list:
        #         #     yield scrapy.Request(url=store, callback=self.parse_page)

            
        #     def get_page_block(self, response1):
        #         page_blocks = response1.xpath('//div[@id="myo-packing-slips"]/div').extract()
        #         for page_block in page_blocks:
        #             self.get_product_block(html.fromstring(page_block))
        #         # self.get_product_block(html.fromstring(page_blocks[0]))
        #         tkMessageBox.showinfo("Result", "End!")
        #         self.driver.close()
        #         os._exit

        #     def get_product_block(self, pageblock):
        # # #ORDER ID 
        #         string_orderID = pageblock.xpath("//div[contains(@class, 'a-section myo-orderId')]/text()")[0].strip().split(":")[1].strip()
        #         global current_orderID
        #         current_orderID = string_orderID
        #         # print("\n AAAAAAAA: " + string_orderID)
        # # #SHIPPING INFORMATION
        #     #ADDRESS
        #         shipAddress_name = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]/span[@id='myo-order-details-buyer-address']/text()")[0].strip()
        #         shipAddress_street = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]/span[@id='myo-order-details-buyer-address']/text()")[1].strip()
        #         shipAddress_city = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]/span[@id='myo-order-details-buyer-address']/text()")[2].strip().split(',')[0]
        #         shipAddress_state = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]/span[@id='myo-order-details-buyer-address']/text()")[3].strip()
        #         shipAddress_zipcode = pageblock.xpath("//div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')]/span[@id='myo-order-details-buyer-address']/text()")[4].strip()
                
        #         global current_address_ship_name, current_address_ship_street, current_address_ship_city, current_address_ship_state, current_address_ship_zipcode
        #         current_address_ship_name = shipAddress_name
        #         current_address_ship_street = shipAddress_street
        #         current_address_ship_city = shipAddress_city
        #         current_address_ship_state = shipAddress_state
        #         current_address_ship_zipcode = shipAddress_zipcode
        #         # print("\n BBBBBBBBB: " + shipAddress_name + " : " + shipAddress_street + " : " + shipAddress_city + " : " + shipAddress_state + " : " + shipAddress_zipcode)
        #     # #ORDER DATE
        #         string_orderDate = pageblock.xpath("//div[contains(@class, 'a-column a-span8 a-span-last')]/div[contains(@class, 'a-section a-spacing-none a-spacing-top-micro a-padding-none')][1]/span/text()")[0].strip()
        #         cstrdate = datetime.strptime(string_orderDate, '%a, %b %d, %Y')
        #         outdate = datetime.strftime(cstrdate, '%m/%d/%Y')
        #         global current_orderDate
        #         current_orderDate = outdate
        #         # print("\n CCCCCCCCC: " + string_orderDate)
        #     # #INFO BLOCK
        #         info_blocks = pageblock.xpath("//table[contains(@class, 'a-normal a-spacing-none a-spacing-top-small table-border')]/tbody/tr")
        #         item_count = 2
        #         print("KSSSSSSSSSSSSSSSSSSSSSSSSSSSS:   " + str(len(info_blocks)))

        #         len_b = len(info_blocks)
        #         if len_b == 0:
        #             # info_block = pageblock.xpath("//table[contains(@class, 'a-normal a-spacing-none a-spacing-top-small table-border')]/tbody/tr")
        #             self.get_item_block(pageblock, item_count)
        #         else:
        #             del info_blocks[0]
        #             for info_block in info_blocks:
        #                 self.get_item_block(info_block, item_count)
        #                 item_count +=1

        # #PRODUCT DETAIL (*******  NEEDS LOOPING COURSE  ********)


        #     def get_item_block(self, infoblock, itemcount):
        #     #QTY
        #         string_qty = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-center table-border')][1]/text()")[0].strip()
        #         # print("QQQQQQQQQQQQTTTTTTTTYYYYYYYYYYY:  " + string_qty)
        #     #SKU
        #         string_sku = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-row')][1]/span[2]/text()")[0].strip()
        #         global current_sku
        #         current_sku = string_sku
        #         # print("BBBBBBBBBBBBBBB: "+string_sku)
        #     #Personalization
        #         string_personalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li[1]/span[contains(@class, 'a-list-item')]/span[2]/text()")[0]
        #         global current_personalization
        #         current_personalization = string_personalization
        #         # print("BBBBBBBBBBBBBBB: "+string_personalization)

        #     #RePersonalization
        #         string_repersonalization = infoblock.xpath("//tr["+str(itemcount)+"]/td[contains(@class, 'a-text-left table-border')]/div[contains(@class, 'a-section a-spacing-none a-padding-none')]/ul[contains(@class, 'a-unordered-list a-nostyle a-vertical')]/li[2]/span[contains(@class, 'a-list-item')]/span[2]/text()")[0]
        #         global current_repersonalization
        #         current_repersonalization = string_repersonalization
        #         # print("BBBBBBBBBBBBBBB: "+string_repersonalization)
        #         # global all_item_count = all_item_count + 1

        #         print("\n  CURRENT: "+ current_orderID + " : "+current_address_ship_name + " : " + current_address_ship_street + " : " + current_address_ship_city + " : " + current_address_ship_state + " : " + current_address_ship_zipcode + " : " + current_sku + " : " + current_orderDate + " : " + current_personalization + " : " + current_repersonalization)

        #         time.sleep(1)
        #         item = AmazonsellerItem()
        #         item['PCAOrder'] = current_orderID
        #         item['CustName'] = current_address_ship_name
        #         item['CustRef1'] = current_address_ship_street
        #         item['CustRef2'] = ""
        #         item['CustStreet'] = ""
        #         item['CustCity'] = current_address_ship_city
        #         item['CustState'] = current_address_ship_state
        #         item['CustZip'] = current_address_ship_zipcode
        #         item['ShipName'] = current_address_ship_name
        #         item['ShipRef1'] = ""
        #         item['ShipRef2'] = ""
        #         item['ShipStreet'] = current_address_ship_street
        #         item['ShipCity'] = current_address_ship_city
        #         item['ShipState'] = current_address_ship_state
        #         item['ShipZip'] = current_address_ship_zipcode
        #         item['Item'] = current_sku
        #         item['Qty'] = string_qty
        #         item['ItemDescription'] = ""
        #         item['Name'] = current_personalization
        #         item['Item1'] = ""
        #         item['Qty1'] = ""
        #         item['ItemDescription1'] = ""
        #         item['Name1'] = ""
        #         item['Item2'] = ""
        #         item['Qty2'] = ""
        #         item['ItemDescription2'] = ""
        #         item['Name2'] = ""
        #         item['Item3'] = ""
        #         item['Qty3'] = ""
        #         item['ItemDescription3'] = ""
        #         item['Name3'] = ""
        #         item['Item4'] = ""
        #         item['Qty4'] = ""
        #         item['ItemDescription4'] = ""
        #         item['Name4'] = ""
        #         item['Item5'] = ""
        #         item['Qty5'] = ""
        #         item['ItemDescription5'] = ""
        #         item['Name5'] = ""
        #         item['Item6'] = ""
        #         item['Qty6'] = ""
        #         item['ItemDescription6'] = ""
        #         item['Name6'] = ""
        #         item['Item7'] = ""
        #         item['Qty7'] = ""
        #         item['ItemDescription7'] = ""
        #         item['Name7'] = ""
        #         item['Date'] = current_orderDate
        #         item['POBox'] = ""
        #         item['PCItemNo'] = ""
        #         item['Place'] = ""
        #         item['Phone'] = ""

        #         # item['Shipping_OrderDate'] = current_orderDate
        #         # # item['SKU'] = current_sku
        #         # item['Personalization'] = current_personalization
        #         # item['Repersonalization'] = current_repersonalization

        #         # yield item
        #         # global items
        #         # items.append(item)
                

        #         with open('C:\CSV\APP\data.csv', 'a') as csvfile:
        #             # fieldnames = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"]
        #             fieldnames = ["PCAOrder", "CustName", "CustRef1", "CustRef2", "CustStreet", "CustCity", "CustState", "CustZip", "ShipName", "ShipRef1", "ShipRef2", "ShipStreet", "ShipCity", "ShipState", "ShipZip", "Item", "Qty", "ItemDescription", "Name", "Item1", "Qty1", "ItemDescription1", "Name1", "Item2", "Qty2", "ItemDescription2", "Name2", "Item3", "Qty3" ,"ItemDescription3", "Name3", "Item4", "Qty4", "ItemDescription4", "Name4", "Item5", "Qty5", "ItemDescription5", "Name5", "Item6", "Qty6", "ItemDescription6", "Name6", "Item7", "Qty7", "ItemDescription7", "Name7", "Date", "POBox", "PCItemNo", "Place", "Phone"]
        #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        #             writer.writerow(item)
        #             csvfile.close()
        #         # global hflag
        #         # if hflag == 'no':
        #         #     writer.writeheader()
        #         # else:
        #         #     writer.writerow(item)
        #             # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        #             # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

        #         # print(str(item))
                
        #         pass

        #         # fields = ["OrderID", "Shipping_Name", "Shipping_Street", "Shipping_City", "Shipping_State", "Shipping_ZipCode", "Shipping_OrderDate", "SKU", "Personalization", "Repersonalization"] # define fields to use
        #         # with open('hi.csv','a+') as f: # handle the source file
        #         #     # f.write("{}\n".format('\t'.join(str(field) 
        #         #     #                         for field in fields))) # write header 
        #         #     # for item in items:
        #         #     f.write("{}\n".format('\t'.join(str(item[field]) 
        #         #                             for field in fields))) # write items
        #         # file = open('%s_%s.csv' % (spider.name, datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')), 'w+b')

        # #     def parse(self, response):

        # #         # start_urls = ['http://localhost/emulatedurl/amazon.html']

        # #         # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        # #         # page = requests.get("http://localhost/emulatedurl/amazon.html")
        # #         page = requests.get("http://localhost/emulatedurl/index.htm")
        # #         # print(page)
        # #         #main_title = response.css('attr(title)')
        # #         #main_price = response.css('.main-price::text').extract()

        # #         # main_image = response.css("img::attr(data-img)").extract()



        # #         sitems1 = response.xpath('//table/tbody//td[1]/text()').extract()
        # #         sitems2 = response.xpath('//table/tbody//td[2]/text()').extract()
        # #         sitems3 = response.xpath('//table/tbody//td[3]/text()').extract()
        # #         sitems4 = response.xpath('//table/tbody//td[4]/text()').extract()
                
        # #         # print(self.format(items[0].strip()))


        # #         for sitem1 in sitems1:
        # #             item = AmazonsellerItem()
        # #             item['num'] = sitem1

        # #             # print(my_item)
        # #             yield item

        # #         for sitem2 in sitems2:
        # #             item = AmazonsellerItem()
        # #             item['type_'] = sitem2

        # #             # print(my_item)
        # #             yield item
        # #         # print(items)





        # # #ORDER ID 
        # #         string_orderID = response.xpath('//div[@class="a-section myo-orderId"]/text()').extract()
        # #         # print(test_block)

        # # #BUYER INFORMATION
        # #     #ADDRESS
        # #         buyerAddress_block = response.xpath('//span[@id="myo-order-details-buyer-address"]').extract()
        # #         buyerAddress_1 = remove_tags(self.format(buyerAddress_block[0]))
        # #         buyerAddress = buyerAddress_1.replace('\n','').strip().replace('  ',' ').strip()
        # #         # print(buyerAddress)
        # #     # ORDER DATE
        # #         string_orderDate = response.xpath('//div[@id="myo-packing-slip-0"]/div[4]/div/div[2]/div/div[2]/div[1]/span/text()').extract()
        # #         # print(string_orderDate[0])

        # # #PRODUCT DETAIL (*******  NEEDS LOOPING COURSE  ********)
        # #     #SKU
        # #         pre_sku = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[1]/span[2]/text()').extract()
        # #         string_SKU = pre_sku[0].replace('\n','').strip()
        # #         # print(string_SKU)
        # #     #Personalization
        # #         pre_personalization = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[6]/ul/li[1]/span/span[2]/text()').extract()
        # #         string_personalization = pre_personalization[0].replace('\n','').strip()
        # #         # print(string_personalization)

        # #     #RePersonalization
        # #         pre_repersonalization = response.xpath('//div[@id="myo-packing-slip-0"]/table/tbody/tr[2]/td[2]/div[6]/ul/li[2]/span/span[2]/text()').extract()
        # #         string_repersonalization = pre_repersonalization[0].replace('\n','').strip()
        # #         # print(string_repersonalization)

        # #         # test_string = response.selector.xpath("//span").extract()
        # #         # print(test_string)

        # #         # #Give the extracted content row wise
        # #         # for item in zip(main_image):
        # #         #     #create a dictionary to store the scraped info
        # #         #     scraped_info = {
        # #         #         'MainImage' : item[0],
        # #         #     }

        # #         #     #yield or give the scraped info to scrapy
        # #         #     yield scraped_info

        # #         pass

            
        # #     def format(self, item):
        # #             try:
        # #                 return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
        # #             except:
        # #                 return ''











        # # from __future__ import unicode_literals
        # # import scrapy
        # # import json
        # # import os
        # # from scrapy.spiders import Spider
        # # from scrapy.http import FormRequest
        # # from scrapy.http import Request
        # # from chainxy.items import ChainItem
        # # from lxml import etree
        # # from selenium import webdriver
        # # from lxml import html
        # # # import usaddress
        # # import pdb

        # # class todo2(scrapy.Spider):
        # # 	name = 'todo2'
        # # 	domain = ''
        # # 	history = []

        # # 	def __init__(self):
        # # 		self.driver = webdriver.Chrome("./chromedriver")
        # # 		script_dir = os.path.dirname(__file__)
        # # 		file_path = script_dir + '/geo/US_States.json'
        # # 		with open(file_path) as data_file:    
        # # 			self.location_list = json.load(data_file)

        # # 	def start_requests(self):
        # # 		init_url = ''
        # # 		yield scrapy.Request(url=init_url, callback=self.body)
            
        # # 	def body(self, response):
        # # 		self.driver.get("http://www.factory-connection.com/find-a-store")
        # # 		self.driver.find_element_by_id('state').send_keys('state')
        # # 		self.driver.find_element_by_xpath('//button').click()
        # # 		source = self.driver.page_source.encode("utf8")
        # # 		tree = etree.HTML(source)
        # # 		store_list = tree.xpath('//section//div[contains(@class, "stores")]//a[2]/@href')
        # # 		for store in store_list:
        # # 			yield scrapy.Request(url=store, callback=self.parse_page)

        # # 	def parse_page(self, response):
        # # 		try:
        # # 			item = ChainItem()
        # # 			detail = self.eliminate_space(response.xpath('//div[contains(@class, "address")]//text()').extract())
        # # 			item['store_name'] = ''
        # # 			item['store_number'] = ''
        # # 			item['address'] = self.validate(detail[0])
        # # 			addr = detail[1].split(',')
        # # 			item['city'] = self.validate(addr[0].strip())
        # # 			sz = addr[1].strip().split(' ')
        # # 			item['state'] = ''
        # # 			item['zip_code'] = self.validate(sz[len(sz)-1])
        # # 			for temp in sz[:-1]:
        # # 				item['state'] += self.validate(temp) + ' '
        # # 			item['phone_number'] = detail[2]
        # # 			item['country'] = 'United States'
        # # 			h_temp = ''
        # # 			hour_list = self.eliminate_space(response.xpath('//div[contains(@class, "hours")]//text()').extract())
        # # 			cnt = 1
        # # 			for hour in hour_list:
        # # 				h_temp += hour
        # # 				if cnt % 2 == 0:
        # # 					h_temp += ', '
        # # 				else:
        # # 					h_temp += ' '
        # # 				cnt += 1
        # # 			item['store_hours'] = h_temp[:-2]
        # # 			yield item	
        # # 		except:
        # # 			pdb.set_trace()		

        # # 	def validate(self, item):
        # # 		try:
        # # 			return item.strip()
        # # 		except:
        # # 			return ''

        # # 	def eliminate_space(self, items):
        # # 		tmp = []
        # # 		for item in items:
        # # 			if self.validate(item) != '' and 'STORE HOURS:' not in self.validate(item):
        # # 				tmp.append(self.validate(item))
        # # 		return tmp
