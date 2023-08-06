import argparse
import os
from stalkoverflow import parsers
from stalkoverflow import handler
from stalkoverflow import ui
from stalkoverflow.color import bcolors
import sys

def main():
    parser = argparse.ArgumentParser (prog='DeBuggy',description='Command-line tool that automatically searches Google and displays results in your terminal when you get a compiler error.\n Made by @Derhnyel')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("-s","--script",help="Run Script from Terminal")
    parser.add_argument('-q','--query',help='Query stackoverflow with Error message ')
    subparser = parser.add_subparsers(dest='command')
    call = subparser.add_parser('call')
    call.add_argument("-id",'--pid',required=True)
    call.add_argument('-e','--err',required=True)
    args = parser.parse_args()


    if args.command=='call':
        if os.path.isfile(args.err):
            ProcessId= int(args.pid)
            handler.execute(args.err,ProcessId)
        else:
            raise Exception("-e takes path to Error logfile Only")    
    elif args.query is not None:
        if not os.path.isfile(args.query):
            query = args.query+' site:stackoverflow.com'
            titles,_,links,_=parsers.GSearch(query)
            if titles != []:
                ui.start_app(links,titles) # Opens interface        
            else:
                print("\n%s%s%s" % (bcolors.red, "No Google results found.\n", bcolors.end))
        else:
             raise Exception("-q takes str and not paths")
    elif args.script is not None:
        handler.ProcessScript(args.script)

    else:
        parser.print_help(sys.stderr)  

if __name__ == '__main__':
    main()