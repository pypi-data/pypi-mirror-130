"""
Getting subparsers to work. A couple of command line options to get the two
functions to work:

    python subparser_play.py print1 --msg1 aloha!
    python subparser_play.py print2 --msg1 hi --msg2 "what are you doing here"

Add this to the list of things I could do for medium articles.

"""
import argparse


def print_one(msg1):
    print(msg1)


def print_two(msg1, msg2):
    print(msg1)
    print(msg2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="how do subparsers work?")
    subparsers = parser.add_subparsers(dest='func')

    one_parser = subparsers.add_parser('print1')
    one_parser.add_argument("--msg1", required=True)

    two_parser = subparsers.add_parser('print2')
    two_parser.add_argument("--msg1", required=True)
    two_parser.add_argument("--msg2", required=True)

    args = parser.parse_args()

    if args.func == 'print1':
        print_one(args.msg1)
    elif args.func == 'print2':
        print_two(args.msg1, args.msg2)
    else:
        print("HUH?")
