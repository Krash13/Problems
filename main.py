from Problem import ProblemSituation

def main():
    file_name = input("Введите путь к файлу:")
    problem=ProblemSituation(file_name)
    problem.play()

main()
