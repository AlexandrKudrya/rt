def main(class_, name, suname):
    arr_tests = []
    arr_correct_tests = [i for i in arr_tests if i.split("_")[-1] == str(class_)]
    print("Chose your test")
    for i in range(len(arr_correct_tests)):
        print(str(i + 1) + ") " + arr_correct_tests[i])
    choisen = int(input())
    test_name = f'tests\\{arr_correct_tests[choisen - 1]}'
    file = open(test_name, mode="r", encoding="utf-8")
    file_arr = file.readlines()
    answers = []
    for i in file_arr:
        i = i.strip(")\n").strip("(").split(",")
        print(i)
        if i[2] == "__Entry__":
            print(i[0])
            ans = input()
        else:
            print(i[0])
            print(*[str(i[2].split(":").index(j) + 1) + ") " + j for j in i[2].split(":")])
            print("write just number of choisen answer")
            ans = input()
        answers.append([i[0], ans])
    fiel = open(f"answers\{name + '_' + suname + '_' + arr_correct_tests[choisen - 1]}", mode="w", encoding="utf-8")
    fiel.write("\n".join(["\t".join(i) for i in answers]))
    fiel.close()
    file.close()

if __name__ == '__main__':
    main(7, "Вася", "Пупкин")