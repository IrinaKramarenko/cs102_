
def read_task():
    #    path = pathlib.Path(path)
    #    with open("tasks.txt") as f:
    #        task = []
    #        for i in range(sum(1 for line in open("tasks.txt", "r"))):
    #            task.append(f.readline())
    #            f = f.replace()
    #            if task[-1] == "task2" or task[-1] == "task3":
    #                break
    #    task.pop(0)
    #    return task
    with open("tasks.txt") as f:
        for line in f:
            while line != "\n":
                if line != "":
                    task.append(line)
                    f = f.replace(line, "")
    task.pop(0)
    return task


# task = ['A -> B', 'B -> C', 'C -> B']


def is_correct(task, result):
    errors = []
    k = 0
    for i in range(len(task)):
        if task[i][-1] != task[i + 1][0] and task[i + 1] <= len(task):
            k += 1
            errors.append(i)
            return False
        if task[i + 1] > len(task) and task[i][-1] != task[0][0]:
            k += 1
            return False
    if k > 1:
        result += "V, V, V...\n"
    return True


def corrector(task, result):
    if not is_correct(task, result):
        copied = task
        copied[errors[0]][-1] = copied[errors[0] + 1][0]
        if is_correct(copied):
            result += copied[errors[0]] + "\n"
        else:
            copied2 = task
            copied2[errors[0] + 1][0] = copied2[errors[0]][-1]
            result += copied[errors[0] + 1] + "\n"
    return result


print(corrector(read_task, corrector(read_task, corrector(read_task, ""))))

