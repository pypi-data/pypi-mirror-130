from insutance.answer import AnswerBot
from insutance.command import CommandParser


def main():
  args = CommandParser().get_args()
  answerbot = AnswerBot()

  if args.name:
    answerbot.print_my_name()
  elif args.age:
    answerbot.print_my_old()
  elif args.github:
    answerbot.print_github_link()
  elif args.blog:
    answerbot.print_blog_link()
  elif args.job:
    answerbot.print_job()
