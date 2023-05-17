from ..itemsloaders import ProductLoader
from ..items import Product
import chompjs
import scrapy



class MenProductsSpider(scrapy.Spider):
    name = "men"

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://www.fjallraven.com/uk/en-gb/men?p={1}",
            callback=self.parse_page,
        )

    def parse_page(self, response):
        products = response.xpath(
            "//div[@class='products--root']/div[contains(@class, 'product--root')]"
        )
        for product in products:
            yield scrapy.Request(
                url=product.xpath(".//h2/a/@href").get(), callback=self.parse_product
            )
        next = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next:
            yield scrapy.Request(
                url=next,
                callback=self.parse_page
            )

    def parse_product(self, response):
        scripts = response.css("script::text").getall()
        for script in scripts:
            if "variants" in script:
                data = chompjs.parse_js_object(script)
                product = ProductLoader(Product(), data)
                product.add_value("name", data["variants"][0]["displayName"])
                product.add_value("price", data["variants"][0]["regularPrice"])
                product.add_value("color", data["variants"][0]["colorName"])
                product.add_value("isNew", data["variants"][0]["isNew"])
                in_stock = False
                if data["variants"][0]["stockInformation"] == "In Stock":
                    in_stock = True
                product.add_value("inStock", in_stock)
                product.add_value("variants", len(data["variants"]))
                yield product.load_item()
