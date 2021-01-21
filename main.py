import praw
import config
import csv
import requests


def main():

    # Get a list of all the tickers on NYSE from Yahoo
    NASDAQ_symbols_url = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
    AMEX_symbols_url = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
    NYSE_symbols_url = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
    with requests.Session() as s:
        download = s.get(NYSE_symbols_url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)

    # Setup the reddit scraper
    reddit = praw.Reddit(client_id=config.reddit_client_id, client_secret=config.reddit_client_secret, user_agent=config.reddit_user_agent)
    # get posts from subreddits
    hot_posts = reddit.subreddit('wallstreetbets').hot(limit=100)
    for post in hot_posts:
        print(post.title)


if __name__ == '__main__':
    main()
