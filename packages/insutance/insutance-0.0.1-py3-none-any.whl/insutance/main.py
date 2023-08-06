from insutance.answer import AnswerBot
from insutance.command import CommandParser
from insutance.question_data import QuestionData


def main():
  args = CommandParser().get_args()
  answerbot = AnswerBot()

  if args.question is None:
    answerbot.print_question_is_none()
  else:
    question = args.question.lower()
    if question in QuestionData["QnAList"]:
      answerbot.print_question_list()

    elif question in QuestionData["Name"]:
      answerbot.print_my_name()

    elif question in QuestionData["Age"]:
      answerbot.print_my_old()

    elif question in QuestionData["ReallyAge"]:
      answerbot.print_really_my_old()
