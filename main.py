from Problem import ProblemSituation

def main(file_name):
    problem=ProblemSituation(file_name)
    problem.play(1)


file_name=input()
main(file_name)
