import argparse
import sys
from tabulate import tabulate
import collecting_articles as colart
import article_extraction as extract
from tqdm import tqdm
from multiprocessing import Pool
import logging

class Gallica :
    """A CLI class wrapping commands for searching and retrieving articles on gallica
    """

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
        parser.add_argument("-r","--ref",help="reference of the searched newspaper")
        parser.add_argument("-n","--newspaper",help="name of the searched newspaper")
        parser.add_argument("-i","--issue",help="reference of the issue")
        parser.add_argument("--start",type=int,help="year to start searching articles for (default 1900)")
        parser.add_argument("--end",type=int,help="year up to which articles should be searched for (default 1950)")
        parser.add_argument("--dir",help="""name of the directory to put issues in. 
            if not set :
                with --issue : print the issue to stdout
                with --ref or --newspaper : print all references to stdout""")
        args = parser.parse_args(stringArgs)
        yearStart = 1900
        yearEnd = 1950
        if args.start :
            yearStart = args.start
        if args.end : 
            yearEnd = args.end
        if (int(args.ref!=None) + int(args.newspaper!=None) + int(args.issue!=None) != 1) :
            print("exactly one of the --ref, --newspaper or --issue arguments must be given")
        else :
            if args.issue is not None :
                fetch_one_issue(args)
            else:
                fetch_all_issues(args,yearStart,yearEnd)
                
#Helper functions
def scrap_issue(*args):
    """
    Helper for scrapping task paralellization
    """
    ref = args[0]
    directory = args[1]
    try :
        issue = colart.get_issue_by_ref(ref)
        extract.store_articles(issue,directory)
    except :
        logging.info(f"invalid fromat for reference : {ref}")

def fetch_one_issue(args):
    """
    Fetch one issue, store it or print it given args
    """
    issue = colart.get_issue_by_ref(args.issue)
    if args.dir :
        extract.store_articles(issue,args.dir)
    else :
        articles = extract.get_articles(issue["raw_text"])
        print("issue retrieved : ")
        print(f"newspaper : {issue['newspaper']}")
        print(f"date : {issue['date']}")
        print("\n")
        for article in articles :
            print(f"title : {article['title']}")
            print(article["text"])
            print("\n")

def fetch_all_issues(args,yearStart,yearEnd):
    """
    Fetch all issues, store them or print them given the args
    """
    if (args.ref) :
        refs = colart.get_issues_reference_by_newspaper_ref(args.ref,yearStart,yearEnd)
    else :
        refs = colart.get_issues_reference_by_name(args.newspaper,yearStart,yearEnd)
    if (args.dir) :
        p = Pool(8)
        tasks = []
        pbar=tqdm(total=len(refs))
        for ref in refs :
            tasks.append(p.apply_async(scrap_issue,(ref,args.dir),callback=lambda x:pbar.update()))
        for task in tasks:
            task.get()
    else :
        print("\n".join(refs))

if __name__ == "__main__":
    Gallica()
