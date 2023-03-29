import os
import pandas as pd
import re
import subprocess

INPUT_FILE = os.path.join(os.path.dirname(__file__), "output.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "processed.csv")


def row_id(row):
    return f"09-{row.name + 1}"


def account_handle(row):
    return f"@{row['username']}"


def date_posted(row):
    created_at = row['created_at']
    result = re.search(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) PST", created_at)
    year, month, day, hour, minute, _ = result.groups()
    return f"{day}/{month}/{year} {hour}:{minute}"


user_info_hash = {}


def generate_user_info(row):
    if row.username not in user_info_hash:
        result = subprocess.getoutput(f"snscrape --jsonl --with-entity --max-results 0 twitter-user {row.username}")
        df = pd.read_json(result, lines=True)
        user_info_hash[row.username] = df.to_dict()


def account_bio(row):
    return user_info_hash[row.username]["description"][0]


def joined(row):
    date_string = user_info_hash[row.username]["created"][0]
    result = re.search(r"(\d{4})-(\d{2})-(\d{2}).*", date_string)
    year, month, _ = result.groups()
    return f"{month}/{year[2:]}"


def following(row):
    return user_info_hash[row.username]["friendsCount"][0]


def followers(row):
    return user_info_hash[row.username]["followersCount"][0]


def location(row):
    return user_info_hash[row.username]["location"][0]


def tweet_type(row):
    labels = []
    
    words = list(filter(lambda word: word[0] != '@', row.tweet.split()))
    if len(words) >= 1:
        labels.append("Text")
    
    photos = row.photos[1:-1]
    if len(photos) >= 1:
        labels.append("Image")

    video = int(row.video)
    if video == 1 and video not in photos:
        labels.append("Video")

    urls = row.urls[1:-1]
    if len(urls) >= 1:
        labels.append("URL")
    
    retweet = bool(row.retweet)
    if retweet:
        labels.append("Retweet")
    
    quote_url = row.quote_url
    if "https" in str(quote_url):
        labels.append("Quote Tweet")

    reply_to = row.reply_to[1:-1]
    if len(reply_to) >= 1:
        labels.append("Reply")

    return ", ".join(labels)


def main():
    if not os.path.exists(INPUT_FILE):
        print("Make sure you've run scrape.py!")
        exit()
    df = pd.read_csv(INPUT_FILE)

    for _, row in df.iterrows():
        generate_user_info(row)

    df["ID"] = df.apply(lambda row: row_id(row), axis=1)
    df["Account handle"] = df.apply(lambda row: account_handle(row), axis=1)
    df["Tweet Type"] = df.apply(lambda row: tweet_type(row), axis=1)
    df["Date posted"] = df.apply(lambda row: date_posted(row), axis=1)
    df["Account bio"] = df.apply(lambda row: account_bio(row), axis=1)
    df["Joined"] = df.apply(lambda row: joined(row), axis=1)
    df["Following"] = df.apply(lambda row: following(row), axis=1)
    df["Followers"] = df.apply(lambda row: followers(row), axis=1)
    df["Location"] = df.apply(lambda row: location(row), axis=1)

    df = df.assign(Group="09")
    df = df.assign(Collector="Ko, Daryll")
    df = df.assign(Category="RBRD")
    df = df.assign(Topic="Leni's incompetence as VP")

    df["Tweet URL"] = df["link"]
    df["Account name"] = df["name"]
    df["Tweet"] = df["tweet"]
    df["Likes"] = df["likes_count"]
    df["Replies"] = df["replies_count"]
    df["Retweets"] = df["retweets_count"]

    final_rows = [
        "ID",
        "Tweet URL",
        "Group",
        "Collector",
        "Category",
        "Topic",
        # Keywords
        "Account handle",
        "Account name",
        "Account bio",
        # (Account type)
        "Joined",
        "Following",
        "Followers",
        "Location",
        "Tweet",
        #   [Tweet Translated]
        "Tweet Type",
        "Date posted",
        #   [Screenshot]
        # (Content type)
        "Likes",
        "Replies",
        "Retweets",
        #   [Quote Tweets]
        #   [Views]
        #   [Rating]
        # (Reasoning)
        #   [Remarks]
        #   [Reviewer]
        #   [Review]
    ]

    final_df = df[final_rows].copy()
    final_df.to_csv(OUTPUT_FILE)


if __name__ == "__main__":
    main()
