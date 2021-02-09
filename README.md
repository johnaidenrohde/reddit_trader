Reddit Trader
===

We've decided to take investment advice from the good people of reddit. Specifically r/wallstreetbets

This app scrapes reddit and makes buy and sell decisions based on the numbers of mentions of a particular ticker. 

Inspired by:

- https://github.com/RyanElliott10/wsbtickerbot
- https://www.swaggystocks.com/dashboard/wallstreetbets/ticker-sentiment
- https://www.reddit.com/r/wallstreetbets/comments/l1839h/gme_announcement/?utm_source=share&utm_medium=mweb

Installation
---

These basic installation instructions are given for Linux machines. Exact setup will vary for Windows and Mac. 

1. Install [Python 3+](https://www.python.org/downloads/) on your machine
2. Install [Git](https://git-scm.com/downloads) on your machine
3. Install the Python virtual environment package `python3 -m pip install venv`
4. Clone the project into a directory that makes you happy
5. Create a virtual environment for the project
5. Enter that virtual environment
6. Upgrade pip `python -m pip install --upgrade pip`
6. Install the required packages using pip `pip install -r requirements.txt`
7. Create the required Reddit credentials [instructions]()
8. Add those credentials to the config file and rename it `config.py`
8. Make two directories `data` and `site`
9. Run the script
10. Enjoy your new-found wealth!


Resources
---

- Scraping Reddit - https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
- Share prices - https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
- List of symbols - https://stackoverflow.com/questions/25338608/download-all-stock-symbol-list-of-a-market
