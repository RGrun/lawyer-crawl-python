import scrapy
from lawyercrawl.items import LawyercrawlItem


class LawyercrawlSpider(scrapy.Spider):
    name = "lawyer_crawl"
    allowed_domains = ["lawyers.law.cornell.edu"]
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
              "Louisiana", " Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", " Nevada", "New-Hampshire", "New-Jersey", "New-Mexico",
              "New-York", "North-Carolina", "North-Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode-Island", "South-Carolina", "South-Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West-Virginia", "Wisconsin", "Wyoming"]

    states_debug = ["Ohio"]

    start_urls = [
        # to be populated in constructor
    ]

    def __init__(self, **kwargs):
        super(LawyercrawlSpider, self).__init__(**kwargs)

        for state in self.states:
            self.start_urls.append("https://lawyers.law.cornell.edu/lawyers/injury-accident-law/" + state)

    def parse(self, response):

        for lawyer_div in response.xpath("//div[@itemtype='http://schema.org/Person']"):

            # scrape detail page
            detail_page_url = lawyer_div.css("a.mainprofilelink::attr('href')").extract()[0]
            if detail_page_url:
                detail_page_url = response.urljoin(detail_page_url)
                yield scrapy.Request(detail_page_url, self.parse_detail_page)

            # paginate to next page
            next_page = response.css("div.pagination > span.next > a::attr('href')")
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse)


    def parse_detail_page(self, response):

        item = LawyercrawlItem()

        cur_state = response.xpath("//nav[@id='breadcrumbs']/a[2]/text()").extract()[0]

        # lawyer's name
        l_name = response.xpath("//*[@id='node-title']/h3/text()").extract()[0]

        # lawyer's phone number
        l_phone = response.css(
            'div.keyinfo strong::text'
        ).extract()
        l_phone = l_phone[0] if len(l_phone) > 0 else "None Listed"

        # lawyer's website URL
        l_site = response.xpath('//*[@id="website_blogs"]/h5/a/@href').extract()
        l_site = l_site[0] if len(l_site) > 0 else "None Listed"

        # lawyer's image URL
        l_image = response.xpath('//*[@id="profileimg"]/div/img/@src').extract()[0]

        # lawyer's location info\

        # assemble location info from table

        #address location blocks
        addressNum = 1
        iterator = 0
        item["lawyer_addresses"] = {}
        for block in response.xpath('//div[@itemprop="workLocation"]'):
            try:
                #print block, addressNum
                street_address_1 = block.xpath('//div[@class="street-address"]/text()').extract()[iterator]

                street_address_2 = block.xpath('//div[@class="street-address-2"]/text()').extract()
                street_address_2 = street_address_2[iterator] if len(street_address_2) > 0 else "None"

                city = block.xpath('//span[@class="locality"]/text()').extract()[iterator]
                state_abbr = block.xpath('//span[@class="region"]/text()').extract()[iterator]
                zip = block.xpath('//span[@class="postal-code"]/text()').extract()[iterator]


                item["lawyer_addresses"]["address" + str(addressNum)] = {
                    "street_address_1" : street_address_1,
                    "street_address_2" : street_address_2,
                    "city" : city,
                    "state_abbr" : state_abbr,
                    "zip" : zip
                }
                addressNum += 1
                iterator += 1
            except:
                continue


        # lawyer's current firm
        l_firm = response.css('span.law_firm > span::text').extract()
        l_firm = l_firm[0] if len(l_firm) > 0 else "None Listed"


        item['lawyer_name'] = l_name
        item['lawyer_phone'] = l_phone
        item['lawyer_site'] = l_site
        item['lawyer_image_url'] = l_image
        item['lawyer_state'] = cur_state
        item['lawyer_firm'] = l_firm
        item['lawyer_cornell_url'] = response.url
        yield item


