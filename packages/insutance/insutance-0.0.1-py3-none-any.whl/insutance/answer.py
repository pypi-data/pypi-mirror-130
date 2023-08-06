import time

from insutance.question_data import QuestionData


class AnswerBot:
  def print_answer_slowly(self, answer):
    for answer in answer.split("\n"):
      print(answer.strip())
      if answer.strip() != "":
        time.sleep(1)

  def print_question_list(self):
    print(
        f"""
      모든 질문을 할 때는 따옴표('')를 붙여주세요:)
      ---------------------------------------------
      # NAME: {QuestionData["Name"]}

      # AGE: {QuestionData["Age"]}
      """
    )

  def print_question_is_none(self):
    answer = """
      저에게 궁금한 것이 없나요..?

      제 이름이 궁금하지는 않나요 ?!
      궁금하다면 "what's your name?" 이라고 물어봐주세요 !
    """
    self.print_answer_slowly(answer)

  def print_my_name(self):
    answer = """
      제 이름은 insutance 에요:)
      그 외에도 다른 닉네임으로도 활동하고 있어요!
      '최낙타', 'camellionchild'

      저의 본명은 알려드리지 않을거에요!
    """
    self.print_answer_slowly(answer)

  def print_my_old(self):
    answer = """
      제 나이가 궁금하시군요!
      몇 살처럼 보이나요 ?!

      제 나이는 ..!
      두구두구두구두구두구두구두구두구두구두구두구....

      비밀~!
      생일만 알려드릴게요!
      저의 생일은 11월 11일 빼빼로데이 입니다!      
      
      정말로 제가 몇 살인지 궁금하다면 아래 문구로 저에게 다시 물어봐주세요:)
      "i really want to know how old you are"
      or
      "나는 진심으로 너가 몇 살인지 궁금해"
    """
    self.print_answer_slowly(answer)

  def print_really_my_old(self):
    answer = """
      힝! 속았지?!
      안 알려드릴거에요!
    """
    self.print_answer_slowly(answer)
