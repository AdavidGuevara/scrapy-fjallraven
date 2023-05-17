from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()

class FjallravenPipeline:
    def __init__(self) -> None:
        self.create_conn()
        self.create_table()

    def create_conn(self):
        self.conn = connect(
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASS"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"],
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS menProducts;""")
        self.curr.execute(
            """
            CREATE TABLE menProducts (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(200),
            price FLOAT,
            color VARCHAR(75),
            isNew BOOLEAN,
            inStock BOOLEAN,
            variants INT,
            PRIMARY KEY(id));
            """
        )

    def store_items(self, item):
        self.curr.execute(
            """INSERT INTO menProducts (name, price, color, isNew, inStock, variants) VALUES (%s, %s, %s, %s, %s, %s)""",
            (item["name"], item["price"], item["color"], item["isNew"], item["inStock"], item["variants"]),
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_items(item)
        return item

    def close_spider(self, spider):
        self.conn.close()


class PriceToUSDPipeline:
    gbpToUsdRate = 1.26

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get("price"):
            priceFloat = float(adapter["price"])
            adapter["price"] = priceFloat * self.gbpToUsdRate
            return item
        else:
            raise DropItem(f"Price not found in: {item}")
