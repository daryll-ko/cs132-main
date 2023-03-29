import os
import twint

c = twint.Config()

c.Username = "jarredsumner"
c.Search = "zig"
c.Output = f"{os.path.dirname(__file__)}/output.txt"
c.Hide_output = True

twint.run.Search(c)
