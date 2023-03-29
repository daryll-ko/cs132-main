import os
import twint

OUTPUT_FILE = f"{os.path.dirname(__file__)}/output.csv"

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

c = twint.Config()

c.Username = "jarredsumner"
c.Search = "zig"

c.Stats = True
c.Hide_output = True
c.Store_csv = True
c.Custom["tweet"] = ["id", "username", "likes_count", "replies_count", "retweets_count"]
c.Output = OUTPUT_FILE

twint.run.Search(c)
