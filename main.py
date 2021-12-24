import math
import sys

weights = []  # веса прдметов
costs = []  # стоимость предметов
obj_list = []  # индексы взятых предметов


def update_weight(mass, weight):
    nod = math.gcd(mass, weight[0])
    for elem in weight:
        nod = math.gcd(nod, elem)

    return int(nod)


def do_table(max_mass, weight_list, cost_list, nod):
    max_mass = int(max_mass / nod)
    for i in range(len(weight_list)):
        weight_list[i] = int(weight_list[i] / nod)

    total_matrix = [[0 for _ in range(max_mass + 1)] for __ in range(len(weight_list) + 1)]

    for i in range(len(weight_list) + 1):
        for j in range(max_mass + 1):

            if i == 0 or j == 0:
                total_matrix[i][j] = 0
                if j == 0:
                    if weight_list[i - 1] == 0:
                        total_matrix[i][j] = cost_list[i - 1]

                continue
            if weight_list[i - 1] > j:
                total_matrix[i][j] = total_matrix[i - 1][j]
                continue
            prev_res = total_matrix[i - 1][j]
            new_res = cost_list[i - 1] + total_matrix[i - 1][j - weight_list[i - 1]]
            total_matrix[i][j] = max(prev_res, new_res)

    return total_matrix


def find_items(total_matrix, i, j):
    if total_matrix[i][j] == 0:
        return
    if total_matrix[i - 1][j] == total_matrix[i][j]:
        find_items(total_matrix, i - 1, j)
    else:
        find_items(total_matrix, i - 1, j - weights[i - 1])
        obj_list.append(i)


def print_answer(total_matrix, obj_list, weight_list, nod, out):
    sum_mass = 0
    for iter in obj_list:
        if iter == 0:
            continue
        sum_mass += weight_list[iter - 1]
    str_ans = str(sum_mass * nod) + ' ' + str(total_matrix[-1][-1])
    print(str_ans, file=out)
    for elem in obj_list:
        print(elem, file=out)


def print_zero_answer(price, obj_list, weight_list, out):
    sum_mass = 0
    for iter in obj_list:
        if iter == 0:
            continue
        sum_mass += weight_list[iter - 1]
    str_ans = str(sum_mass) + ' ' + str(price)
    print(str_ans, file=out)
    for elem in obj_list:
        print(elem, file=out)


def main():
    mass = None

    for line in sys.stdin:
        line = line.rstrip('\r\n')

        if len(line.split()) == 1 and mass is None:
            mass = int(line.split()[0])
            continue

        elif len(line.split()) == 2 and mass is not None:
            if line.split()[0].isdigit() and line.split()[1].isdigit():
                weights.append(int(line.split()[0]))
                costs.append(int(line.split()[1]))
            else:
                print("error", file=sys.stdout)

        # elif line == "end":
        #     break

        elif not (line and line.strip()):
            continue
        else:
            print("error", file=sys.stdout)

    if mass:
        nod = update_weight(mass, weights)

        table = do_table(mass, weights, costs, nod)

        find_items(table, len(table) - 1, len(table[0]) - 1)

        print_answer(table, obj_list, weights, nod, sys.stdout)

    elif weights:
        price = 0
        for i in range(len(weights)):
            if weights[i] == 0:
                obj_list.append(i + 1)
                price += costs[i]
        print_zero_answer(price, obj_list, weights, sys.stdout)


main()
