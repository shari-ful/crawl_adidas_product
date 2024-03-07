import os
from dotenv import load_dotenv
import scraper
import excel_writer


load_dotenv()

SOURCE_URL = os.getenv("SOURCE_URL")

data = scraper.get_item_info(SOURCE_URL)

excel_writer.create_excel_file(data)


