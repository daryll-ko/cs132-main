import argparse
import os
import twint

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "output.csv")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--username", default="jarredsumner")
    parser.add_argument("-s", "--search", default="zig")
    parser.add_argument("-l", "--limit", default="200")

    args = parser.parse_args()

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    c = twint.Config()

    c.Username = args.username
    c.Search = args.search
    c.Limit = int(args.limit)

    c.Hide_output = True
    c.Store_csv = True
    c.Custom["tweet"] = [
        "username",
        "id",
        "name",
        "tweet",
        "created_at",
        "mentions",
        "urls",
        "photos",
        "likes_count",
        "replies_count",
        "retweets_count"
    ]
    c.Output = OUTPUT_FILE

    twint.run.Search(c)


if __name__ == "__main__":
    main()
