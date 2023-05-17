from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    color_in = MapCompose(lambda x: x.lower())
    isNew_in = MapCompose(lambda x: True if x == "true" else False)
    variants_in = MapCompose(lambda x: int(x))
