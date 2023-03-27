# Datenna Developer Assignment - Source Scraping

##### Preface

At Datenna we leverage publicly available sources available on the internet. Pieces of automated software, so-called
scrapers, will "crawl" over the source and obtain pieces of information of interest.

In this assignment, your task is to build such a scraper. The goal of this scraper is to obtain all products listed on a
website, together with their (meta)data/details. This data could hypothetically be used by a price-comparison site,
which
aims to help the user to find the best deal online.

### STEPS FOR RUNNING APPLICATION
1. Open the project root folder in your IDE of choice.
2. Install dependencies in the `requirements.txt` in your virtual environment.
3. Ensure IDE is using created virtual environment.
4. Run `python main.py` with its respected `args` eg: (`python main.py https://site4scraping.nl/`).
5. JSON and CSV files will be in the `scraped_data` folder.


### Project structure

In this project you find:

1. `main.py` which is the entry point of the scraper application. By running `python main.py` with its respected `args`
   the scraper should start executing.
2. Module `scraper_base` with all files that provide a basis (base classes and functionalities) for the scraper
   application.
3. Module `webshop_scraper` where it is your job to create a scraper using the steps below.

### Project setup

**Requirements:** Python 3.9 or above. We will test your submission against Python 3.9.

1. Open the project root folder in your favourite IDE (PyCharm, VS Code, VIM (if you know how to exit it) etc.)
2. This project has a few Python packages as dependencies, you can install them in your virtual environment
   using `requirements.txt` or create a pre-configured virtual environment using `poetry install` (using
   Poetry https://python-poetry.org/). _If you were to use any other dependencies, then please add them to
   requirements.txt or pyproject.toml. You should be able to complete the assignment without any other dependencies._
3. Configure your IDE to use your freshly created virtual environment for better code hinting and inspections.

**Extra note:** One of the tools we use at Datenna to parse scraped `HTML` source code
is [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). We strongly advise you to use this package
to help you parse the HTML in order to find new URLs to scrape and to extract pieces of information to export.

---

### The assignment

Details:
**URL:** https://site4scraping.nl/
**Goal:** Retrieve all product data

1. Identify and create `PageType` classes in `page_types.py` that will instruct the scraper how to handle different kind
   of pages on the website. You only need to create `PageType`s for pages containing product information, including the
   product description. _Ensure that you instruct your PageType to only process results of the actual product pages.
   Also, prevent adding unnecessary jobs to the queue._
2. Create a `ResultProcessor` class that parses the `HTML` of the product pages you have scraped and creates a `CSV`
   or `JSON` with all relevant data about the products, like name, price, sale price product description and stock level
   if available. Adapt `main.py` to use this new `ResultProcessor`.
3. Now we want to be able to prioritise tasks during scraping. Imagine we want to prioritise a certain page type over
   another. Adapt the `scraper_base` module in such a way we can define priorities per page type and higher priority
   tasks are scraped before lower prioritised tasks.
4. The current scraper base implementation does not take erroring requests into account. Now, if the site does not
   respond in time, we don't retry the job at a later time. Adapt the `scraper_base` module in such a way that we retry
   a faulty request at most `N` times.

---

### Notes

- **Since the application is not linked to a database and does not take into account previously visited URLs, it could
  scrape indefinitely. Fixing this is out of the scope of the assignment.**

- The code you write should be fully PEP8 compliant. You may verify that with the linting tool(s) of your choice.

- We expect you to uphold your best programming practices for the completion of this assignment, as if your code would
  end up in production and interact with other software components. A robust solution which covers fewer points will be
  judged more favourably than a complete solution that cuts corners.

- We will check your assignment by doing a full scrape of the website using your scraper and see how the processed
  results look. Please ensure the program is in a finished state that we can execute even though you might not have
  completed it in full.
