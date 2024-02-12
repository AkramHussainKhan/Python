import scrapy


class LaptopSpider(scrapy.Spider):
    name = "laptop"
    start_urls = ["https://www.ryanscomputers.com/category/laptop-all-laptop?limit=100&osp=1&st=0"]

    def parse(self, response):
        laptops = response.xpath('//div[@class = "card-body text-center"]')
        for index, laptop in enumerate(laptops, start=1):
            try:
                processor = response.xpath(f'(//ul[@class="mt-2 mb-2 category-info"]/li[contains(text(), "Processor Type")]/text())[{index}]').get().replace("Processor Type. -","")
            except:
                processor= None
            yield{
                'title': response.xpath(f'(//p[@class="card-text p-0 m-0 list-view-text"]/a/text())[{index}]').get(),
                'url':response.xpath(f'(//div[@class ="card-body text-center"]/a/@href)[{index}]').get(),
                'processor Type': processor,
                'Generation': response.xpath(f'(//ul[@class="mt-2 mb-2 category-info"]/li[contains(text(), "Generation")]/text())[{index}]').get().replace("Generation -",""),
                'Price': response.xpath(f'(//p[@class="pr-text cat-sp-text pb-1"]/text())[{index}]').getall()
            }
        next_page = response.xpath('//a[@aria-label="Next »"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback= self.parse)

