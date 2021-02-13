import praw
import config
import pandas as pd
import numpy
import time
from datetime import datetime
import yfinance as yf
import math
from urllib import error as url_error


def main():
    # Take the start time
    start_time = datetime.now()
    # Request the Reddit posts
    current_UNIX_time = time.time()
    one_day_ago = current_UNIX_time - (24 * 60 * 60)
    post_df = get_post_by_date(subreddit='wallstreetbets', start_time=current_UNIX_time, end_time=one_day_ago)
    # Save the posts to a file
    posts_time = datetime.now()
    print('Posts collected in ' + str(posts_time - start_time))
    post_df.to_csv('./data/' + start_time.strftime("%Y%m%d_%H:%M:%S") + '-posts.csv')
    # Load the list of all the tickers on the AMEX, NASDAQ, and NYSE
    symbol_df = pd.read_csv("./210125-symbols_amex_nasdaq_nyse.csv")
    # Search for the symbols in the posts
    scored_symbols_df = calc_symbol_score(post_df, symbol_df)
    # Load the existing positions
    try:
        old_positions_df = pd.read_csv('./data/positions.csv')
    except FileNotFoundError:
        old_positions_df = None
        print('No existing position file found. Assuming initial investment of $' + str(config.initial_investment_USD))
    # Determine our new position based on these symbols
    new_positions_df = calc_positions(scored_symbols_df, old_positions_df)
    # Save the new positions to a file
    results_time = datetime.now()
    print('Results found in ' + str(results_time - posts_time))
    new_positions_df.to_csv('./data/' + start_time.strftime("%Y%m%d_%H:%M:%S") + '-positions.csv')
    new_positions_df.to_csv('./data/positions.csv')
    # Make an html table
    save_html_positions(new_positions_df)
    # Determine the buys and sells based on the previous portfolio
    orders_df = calc_orders(new_positions_df, old_positions_df)
    orders_df.to_csv('./data/orders.csv')
    # TODO: Perform the buys and sells


def save_html_positions(df):
    # Load the header and footer as strings
    with open('./site/header.html', 'r') as file:
        header = file.read()
    with open('./site/footer.html', 'r') as file:
        footer = file.read()
    # make an html table from the positions dataframe
    df['percentage'] = df['percentage'] * 100
    position_table = df[['symbol', 'score', 'percentage', 'shares', 'ask', 'value']].to_html(classes='styled-table')
    # add a line to show when it was updated
    update_time = '<p>Updated ' + str(datetime.now()) + '</p>'
    # save the whole thing to the site directory
    with open('./site/index.html', 'w') as file:
        file.write(header + update_time + position_table + footer)


def get_post_by_date(subreddit, start_time, end_time):
    """Get Reddit Posts between two dates - returns a pandas dataframe

        Keyword arguments:
        subreddit -- name of the subreddit (default 'all')
        start_time -- date and time in Unix format
        end_time -- date and time in Unix format
    """
    # Setup the reddit scraper
    reddit = praw.Reddit(client_id=config.reddit_client_id,
                         client_secret=config.reddit_client_secret,
                         user_agent=config.reddit_user_agent)
    # Get all the posts
    post_list = []
    posts = reddit.subreddit(subreddit).new(limit=1000)
    for post in posts:
        if post.created >= end_time:
            post_list.append(
                [
                 # post.id,
                 # post.author,
                 post.title,
                 post.score,
                 # post.num_comments,
                 post.selftext,
                 # post.created,
                 # post.pinned,
                 # post.total_awards_received
                 ]
            )
    # Create a dataframe
    post_df = pd.DataFrame(
        post_list,
        columns=[
            # "id",
            # "author",
            "title",
            "score",
            # "comments",
            "post",
            # "created",
            # "pinned",
            # "total awards"
        ]
    )
    return post_df


def calc_symbol_score (post_df, symbol_df):
    """Search reddit posts for stock tickers - returns a pandas dataframe consisting of the symbol and the score

            Keyword arguments:
            post_df -- pandas dataframe of posts from PRAW
            symbol_df -- pandas dataframe with stock symbols in ALL CAPS strings
    """
    # Create a string to search for the stock symbols
    post_df["to_search"] = post_df["title"] + post_df["post"]
    results = {}
    for symbol in symbol_df["Symbol"]:
        # Search the posts (both title and text) for the symbol with a dollar sign
        result = post_df[
            post_df["to_search"].str.contains("$" + symbol + " ", regex=False) |
            post_df["to_search"].str.contains("$" + symbol + ",", regex=False)
            ]
        if not result.empty:
            result = post_df[
                post_df["to_search"].str.contains(" " + symbol + " ", regex=False) |
                post_df["to_search"].str.contains(" " + symbol + ",", regex=False) |
                post_df["to_search"].str.contains("$" + symbol + " ", regex=False) |
                post_df["to_search"].str.contains("$" + symbol + ",", regex=False)
                ]
            # Create sum the score of all the posts that mention the symbol
            points = result["score"].sum()
            results[symbol] = points

    # Made a data frame from the results
    df = pd.DataFrame.from_dict(results, orient='index', columns=['score'])
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'symbol'})
    return df


def calc_positions(scored_symbols_df, old_positions_df):
    """Workout shares to hold - returns a pandas dataframe consisting of the symbol and the score

                Keyword arguments:
                scored_symbols_df -- pandas dataframe tickers with scores
                symbol_df -- pandas dataframe with stock symbols in ALL CAPS strings
    """
    # Rank the symbols we find by the score
    scored_symbols_df = scored_symbols_df.sort_values('score', ascending=False)
    # Determine the percentage of the portfolio the stocks should make up
    scored_symbols_df['total_score'] = scored_symbols_df['score'].sum()
    scored_symbols_df['percentage'] = scored_symbols_df['score'] / scored_symbols_df['total_score']
    # Get the current ask price for each new stonk
    scored_symbols_df['ask'] = scored_symbols_df.symbol.map(lambda x: get_symbol_info(x, 'ask'))
    # Excluded shares with no current asking price
    scored_symbols_df = scored_symbols_df[(scored_symbols_df['ask'] != numpy.NaN)]
    # Determine how much buying power we have right now
    if old_positions_df is None:
        buying_power = config.initial_investment_USD
    else:
        # workout how much cash we have before the next call wrecks the value
        current_cash = old_positions_df.loc[old_positions_df['symbol'] == 'cash', 'value'].values[0]
        # Get the value of all our existing stonk
        old_positions_df['bid'] = old_positions_df.symbol.map(lambda x: get_symbol_info(x, 'ask'))
        old_positions_df['value'] = old_positions_df['bid'] * old_positions_df['shares']
        buying_power = old_positions_df['value'].sum() + current_cash
    # Calculate the max shares
    scored_symbols_df['shares'] = (buying_power * scored_symbols_df['percentage']) / scored_symbols_df['ask']
    # Rounding each one down
    scored_symbols_df['shares'] = scored_symbols_df['shares'].map(lambda x: math.floor(x))
    scored_symbols_df['value'] = scored_symbols_df['shares'] * scored_symbols_df['ask']
    # Workout how much cash we have left
    # We want to save this to cover the fact that, by the time we buy there may have been a lot of price change
    cash_remaining = buying_power - (scored_symbols_df['shares'] * scored_symbols_df['ask']).sum()
    # Save that value as a row with the symbol `cash`
    cash_row = {'symbol': 'cash', 'value': cash_remaining}
    scored_symbols_df = scored_symbols_df.append(cash_row, ignore_index=True)
    # return the result
    return scored_symbols_df


def get_symbol_info(symbol, info):
    try:
        return yf.Ticker(symbol).info[info]
    except url_error.HTTPError:
        return numpy.NaN

def calc_orders(new_df, prev_df):
    if prev_df is None:
        # simple case, if we have no portfolio we just need to buy everything
        orders_df = new_df[['symbol', 'shares']]
    else:
        # join the data frame on their symbol and fill NaN with `0`s
        orders_df = pd.merge(new_df, prev_df, on='symbol', how='outer', suffixes=['', '_old'])
        orders_df = orders_df.fillna(0)
        # subtract the new and old shares
        orders_df['diff'] = orders_df['shares'] - orders_df['shares_old']
        # make buy and sell columns
        orders_df['buy'] = [x if x > 0 else 0 for x in orders_df['diff']]
        orders_df['sell'] = [x * -1 if x < 0 else 0 for x in orders_df['diff']]

    return orders_df[['symbol', 'buy', 'sell']]


if __name__ == '__main__':
    main()
