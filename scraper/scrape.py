import twint

c = twint.Config()

c.Username = "jarredsumner"
c.Search = "zig"

twint.run.Search(c)
