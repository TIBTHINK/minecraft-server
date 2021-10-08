import argparse

parser = argparse.ArgumentParser(
    description="command line interface of this script")


parser.add_argument("-c", "--clean", help="Removes all files exept the init file",
                    action="store_true",)
parser.add_argument("-v", "--version",
                    help="Set the version you want",
                    action="store_true",
                    )
parser.add_argument("-C", "--cores", help="Set how many cores you want the server to use",
                    action="store_true",)
parser.add_argument("-m", "--memory", help="Set how much ram you want to allocate",
                    action="store_true",)

args = parser.parse_args()

if args.version:
    