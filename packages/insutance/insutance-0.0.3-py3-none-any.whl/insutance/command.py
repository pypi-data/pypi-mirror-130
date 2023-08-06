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
    options_group = insutance_parser.add_mutually_exclusive_group(required=True)
    options_group.add_argument("--name", action="store_true", help=f"이름이 뭔가요?")
    options_group.add_argument("--age", action="store_true", help=f"몇 살이에요?")
    options_group.add_argument("--github", action="store_true", help=f"Github 주소가 뭐에요?")
    options_group.add_argument("--blog", action="store_true", help=f"Blog 주소는 뭐에요?")
    options_group.add_argument("--job", action="store_true", help=f"어떤 일을 하시죠?")

    return self.parser.parse_args()
