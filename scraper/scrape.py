import os
import twint

OUTPUT_FILE = f"{os.path.dirname(__file__)}/output.csv"

os.remove(OUTPUT_FILE)

c = twint.Config()

c.Username = "jarredsumner"
c.Search = "zig"

c.Stats = True
c.Hide_output = True
c.Store_csv = True
c.Custom["tweet"] = ["id", "username"]
c.Output = OUTPUT_FILE

twint.run.Search(c)
