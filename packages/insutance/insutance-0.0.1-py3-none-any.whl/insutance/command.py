import argparse


class CommandParser:
  def __init__(self) -> None:
    self.parser = argparse.ArgumentParser(prog="hey")
    self.subparser = self.parser.add_subparsers(
        dest="my_name",
        help="write my name"
    )

  def get_args(self) -> argparse.Namespace:
    insutance_parser = self.subparser.add_parser(
        "insutance",
        help="what do you want to know about me?"
    )
    insutance_parser.add_argument("question", nargs="?", help="write the question")
    return self.parser.parse_args()
