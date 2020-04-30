from Problem import ProblemSituation

def main():
    file_name = input("Введите путь к файлу:")
    problem=ProblemSituation(file_name)
    tim=int(input("Введите работы в минутах:"))
    problem.play(tim)



main()
