# WebShop Scraper

### Web scraper built to retrieve product data from a shop website.

## Project Description
A web scraper that allows you to scrape a website url, built using Python 3 and depends on the requests and BeautifulSoup to extract information from HTML pages.

The scraper will start with the initial URL and crawl through the website, discovering new pages to scrape along the way. The scraper has Page type classes which instruct the scraper on how to get new scraper jobs, determines when to process results and also assigns priority for certain page types. The results are then processed by the ResultProcessor class defined in the  'webshop_scraper.result_processors' module.

### STEPS FOR RUNNING APPLICATION

**Requirements:** Python 3.9 or above.

1. Open the project root folder in your IDE of choice.
2. Install dependencies in the `requirements.txt` in your virtual environment.
3. Ensure IDE is using created virtual environment.
4. Run `python main.py` with its respected `args` eg: (`python main.py https://site4scraping.nl/`). 
5. JSON and CSV files will be in the `scraped_data` folder.

## Extending the Scraper

To extend the scraper to extract data from additional pages, you can create a new page type class in page_types.py. 
The class should inherit from PageTypeBase and should implement the url_matcher, find_new_jobs, and process_result methods.
## Note
Tags and classes used in the PageType classes and ResultProcessor class to extract data from the website need to be checked periodically incase webpage structure changes.

## Contributing
If you find any issues or have any suggestions for improvements, feel free to create an issue or a pull request on the project's GitHub repository.
