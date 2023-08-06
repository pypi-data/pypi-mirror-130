import time


class AnswerBot:
  def print_answer_slowly(self, answer) -> None:
    for answer in answer.split("\n"):
      print(answer.strip())
      if answer.strip() != "":
        time.sleep(1)

  def print_my_name(self) -> None:
    answer = """
      제 이름은 insutance 에요:)
      그 외에도 다른 닉네임으로도 활동하고 있어요!
      '최낙타', 'camellionchild'

      저의 본명은 알려드리지 않을거에요!
    """
    self.print_answer_slowly(answer)

  def print_my_old(self) -> None:
    answer = """
      제 나이가 궁금하시군요!
      몇 살처럼 보이나요 ?!

      제 나이는 ..!
      두구두구두구두구두구두구두구두구두구두구두구....

      비밀~!
      생일만 알려드릴게요!
      저의 생일은 11월 11일 빼빼로데이 입니다!      
    """
    self.print_answer_slowly(answer)

  def print_github_link(self) -> None:
    answer = """
      저의 Github 링크를 알려드릴게요:)
      https://github.com/insutance
    """
    self.print_answer_slowly(answer)

  def print_blog_link(self) -> None:
    answer = """
      저의 Blog 링크를 알려드릴게요:)
      Velog: https://velog.io/@insutance
      Naver: https://blog.naver.com/insutance
    """
    self.print_answer_slowly(answer)

  def print_job(self) -> None:
    answer = """
      2021.03 ~ 현재      라인웍스(정직원, 데이터 엔지니어)

      2020.08 ~ 2020.12   티스쿨컴퍼니(인턴, 백엔드 엔지니어)
    """
    self.print_answer_slowly(answer)
