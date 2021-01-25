import praw
import config
import pandas as pd
import time


def main():
    # Load the list of all the tickers on the AMEX, NASDAQ, and NYSE
    symbols = pd.read_csv("./210125-symbols_amex_nasdaq_nyse.csv")
    print(symbols)
    print(symbols.dtypes)
    # Setup the reddit scraper
    reddit = praw.Reddit(client_id=config.reddit_client_id, client_secret=config.reddit_client_secret,
                         user_agent=config.reddit_user_agent)
    # Get all the posts in the last 24 hours
    current_UNIX_time = time.time()
    one_day_ago = current_UNIX_time - (24*60*60)
    post_list = []
    posts = reddit.subreddit('wallstreetbets').new(limit=1000)
    for post in posts:
        if post.created >= one_day_ago:
            post_list.append(
                [post.id,
                 post.author,
                 post.title,
                 post.score,
                 post.num_comments,
                 post.selftext,
                 post.created,
                 post.pinned,
                 post.total_awards_received
                 ]
            )
    # Create a dataframe
    post_df = pd.DataFrame(
        post_list,
        columns=[
            "id",
            "author",
            "title",
            "score",
            "comments",
            "post",
            "created",
            "pinned",
            "total awards"
        ]
    )
    # Create a string to search for the stock symbols
    post_df["to_search"] = post_df["title"] + post_df["post"]
    results = {}
    for symbol in symbols["Symbol"]:
        # Search the posts (both title and text) for the symbol
        result = post_df[
                            post_df["to_search"].str.contains(" " + symbol + " ", regex=False) |
                            post_df["to_search"].str.contains(" " + symbol + ",", regex=False) |
                            post_df["to_search"].str.contains("$"+ symbol + " ", regex=False) |
                            post_df["to_search"].str.contains("$" + symbol + ",", regex=False)
                        ]
        if not result.empty:
            # Create sum the score of all the posts that mention the symbol
            points = result["score"].sum()
            results[symbol] = points
    # Rank the symbols we find by the score
    results_df = pd.DataFrame.from_dict(results, orient='index', columns=['score'])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(results_df.sort_values('score', ascending=False))
    # Rebalance the portfolio based on these scores


if __name__ == '__main__':
    main()
