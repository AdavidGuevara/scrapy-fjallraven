import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    isNew = scrapy.Field()
    inStock = scrapy.Field()
    variants = scrapy.Field()
