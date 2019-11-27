import argparse
import sys
from tabulate import tabulate

import collecting_articles as colart

class Gallica :

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="A gallica API for retrieving archives",
            usage=""" gallica command [<args>]

The supported commands for this API are :
    search      Finds the reference of the given newspaper
    retrieve    Retrieve all the matching articles
        """)
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self,args.command)(sys.argv[2:])

    def search(self,stringArgs): 
        parser = argparse.ArgumentParser(
            description="Finds the reference of the given newspaper"
        )
        parser.add_argument("title", help="title of the article to be searched for")
        parser.add_argument("-n","--number",help="number of results to be displayed",type=int)
        args = parser.parse_args(stringArgs)
        n = 10
        if args.number is not None :
            n = args.number
        newspapers = colart.get_newspaper_reference(args.title,n)
        print(tabulate(newspapers,headers="keys"))

    def retrieve(self,stringArgs):
        parser = argparse.ArgumentParser(
            description="Retrieve all the matching articles"
        )
        parser.add_argument("-r","--ref",help="reference of the searched article")
        parser.add_argument("--start",type=int,help="year to start searching articles for (default 1900)")
        parser.add_argument("--end",type=int,help="year up to which articles should be searched for (default 1950)")
        args = parser.parse_args(stringArgs)
        yearStart = 1900
        yearEnd = 1950
        if args.start is not None :
            yearStart = args.start
        if args.end is not None : 
            yearEnd = args.end
        references = colart.get_issues_reference_by_newspaper_ref(args.ref,yearStart,yearEnd)
        print("\n".join(references))

if __name__ == "__main__":
    Gallica()
