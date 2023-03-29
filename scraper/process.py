import os
import pandas as pd
import re

INPUT_FILE = os.path.join(os.path.dirname(__file__), "output.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "processed.csv")


def row_id(row):
    return f"09-{row.name + 1}"


def tweet_url(row):
    return f"https://twitter.com/{row['username']}/status/{row['id']}"


def account_handle(row):
    return f"@{row['username']}"


def date_posted(row):
    created_at = row['created_at']
    result = re.search(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) PST", created_at)
    year, month, day, hour, minute, _ = result.groups()
    return f"{day}/{month}/{year} {hour}:{minute}"


def main():
    if not os.path.exists(INPUT_FILE):
        print("Make sure you've run scrape.py!")
        exit()
    df = pd.read_csv(INPUT_FILE)

    df["ID"] = df.apply(lambda row: row_id(row), axis=1)
    df["Tweet URL"] = df.apply(lambda row: tweet_url(row), axis=1)
    df["Account handle"] = df.apply(lambda row: account_handle(row), axis=1)
    df["Date posted"] = df.apply(lambda row: date_posted(row), axis=1)
    
    df = df.assign(Group="09")
    df = df.assign(Collector="Ko, Daryll")
    df = df.assign(Category="RBRD")
    df = df.assign(Topic="Leni's incompetence as VP")

    df["Keywords"] = ""

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
        # Account bio
        # Account type
        # Joined
        # Following
        # Followers
        # Location
        "Tweet",
        # [Tweet Translated]
        # Tweet Type
        "Date posted",
        # [Screenshot]
        # Content type
        "Likes",
        "Replies",
        "Retweets",
        # [Quote Tweets]
        # [Views]
        # [Rating]
        # Reasoning
        # [Remarks]
        # [Reviewer]
        # [Review]
    ]

    final_df = df[final_rows].copy()
    final_df.to_csv(OUTPUT_FILE)


if __name__ == "__main__":
    main()
