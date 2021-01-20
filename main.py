import praw
import config

def main():
    # Setup the reddit scraper
    reddit = praw.Reddit(client_id=config.reddit_client_id, client_secret=config.reddit_client_secret, user_agent=config.reddit_user_agent)

    # get posts from subreddits
    hot_posts = reddit.subreddit('wallstreetbets').hot(limit=100)
    for post in hot_posts:
        print(post.title)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
