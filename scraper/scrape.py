import os
import twint

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "output.csv")

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

c = twint.Config()

c.Username = "jarredsumner"
c.Search = "zig"

c.User_full = True
c.Hide_output = True
c.Store_csv = True
c.Custom["tweet"] = ["username", "id", "name", "tweet", "created_at", "mentions", "urls", "photos", "likes_count", "replies_count", "retweets_count"]
c.Output = OUTPUT_FILE

twint.run.Search(c)
