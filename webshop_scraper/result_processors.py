"""Create here your result processor class."""
from scraper_base.result_processor_base import ResultProcessorBase
from scraper_base.data_models import JobResult
from typing import Optional
import os
import json
import pandas as pd
import numpy as np


class ResultProcessor(ResultProcessorBase):
    """
    Concrete class for processing dataclass objects."""

    json_file_path: Optional[str] = "./scraped_data/data.json"
    csv_file_path: Optional[str] = "./scraped_data/data.csv"

    @staticmethod
    def process_result(obj: JobResult) -> None:
        """Parses HTML and creates JSON/CSV containing product details"""
        soup = obj.get_soup()
        product = soup.find("div", class_=["product", "type-product"])
        is_onsale = False

        # Soup object containing summary of the product
        product_data_container = product.find("div", class_=["summary", "entry-summary"])

        name_container = product_data_container.find("h1", class_=["product_title", "entry-title"]).get_text()
        price_container = product_data_container.find_all("span", class_=["woocommerce-Price-amount", "amount"])
        try:
            price = price_container[0].get_text()
            sale_price = price_container[1].get_text()
        except IndexError:
            try:
                price = price_container[0].get_text()
                sale_price = None
            except IndexError:
                price = None
                sale_price = None
        else:
            is_onsale = True

        description_container = product.find("div", class_="woocommerce-Tabs-panel")
        description = description_container.find("p").get_text()

        stock_level_container = product_data_container.find("p", class_="stock").get_text().strip()

        product_details = {
            "name": name_container,
            "price": price,
            "sale_price": sale_price,
            "on_sale": is_onsale,
            "description": description,
            "stock_level": stock_level_container
        }

        json_data = []

        # Check if the data.json file exists
        if os.path.exists(ResultProcessor.json_file_path):
            # If the file exists, open it and append the data
            with open(ResultProcessor.json_file_path, 'r') as f:
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError:
                    # If the file is empty or not in JSON format, start with an empty list
                    json_data = []
                if product_details not in json_data:
                    json_data.append(product_details)
                else:
                    # product details already exists
                    pass
            with open(ResultProcessor.json_file_path, 'w') as f:
                json.dump(json_data, f, indent=4)
        else:
            # If the file does not exist, create it and write the data
            with open(ResultProcessor.json_file_path, 'w') as f:
                json.dump([product_details], f, indent=4)

        df = pd.DataFrame(json_data)
        df.replace("", np.nan, inplace=True)
        df.fillna("null", inplace=True)
        df.to_csv(ResultProcessor.csv_file_path, index=False, mode="w")
