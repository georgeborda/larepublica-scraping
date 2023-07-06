# Scrapping the news of the day

## How to use

* Clone the repository
* Create the virtual environment 
    `python3 -m venv venv`
* Activate the virtual environment
    `source venv/bin/activate`
* Install the dependencies
    `pip install -r requirements.txt`
* Execute the script
    `python3 scraper.py`

This will create a directory with the date as the name, and for each news item it will create a .txt file with the title, summary and body inside it

The web page may have changed when you use the repository, so you need to fix the XPath expressions and nothing else.