import argparse
import os
import twint

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "output.csv")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--username")
    parser.add_argument("-s", "--search")
    parser.add_argument("-l", "--limit", default="100")
    parser.add_argument("-f", "--fromYear", default="2016")
    parser.add_argument("-t", "--toYear", default="2022")

    args = parser.parse_args()

    if not args.search:
        print("Include a search term!")
        exit()

    if int(args.fromYear) > int(args.toYear):
        print("Make sure -f is less than -t!")
        exit()

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    c = twint.Config()

    if args.username:
        c.Username = args.username
    c.Search = args.search
    c.Limit = int(args.limit)

    c.Hide_output = True
    c.Store_csv = True
    c.Output = OUTPUT_FILE

    c.Since = f"{args.fromYear}-01-01"
    c.Until = f"{args.toYear}-12-31"

    twint.run.Search(c)


if __name__ == "__main__":
    main()
