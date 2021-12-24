import sys

mass = 165
weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]  # веса прдметов
costs = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]  # стоимость предметов
obj_list = list()  # индексы взятых предметов


def do_table(max_mass, weight_list, cost_list):
    total_matrix = [[0 for _ in range(max_mass + 1)] for __ in range(len(weight_list) + 1)]

    for i in range(len(weight_list) + 1):
        for j in range(max_mass + 1):

            if i == 0 or j == 0:
                total_matrix[i][j] = 0
                continue
            if weight_list[i - 1] > j:
                total_matrix[i][j] = total_matrix[i - 1][j]
                continue
            prev_res = total_matrix[i - 1][j]
            new_res = cost_list[i - 1] + total_matrix[i - 1][j - weight_list[i - 1]]
            total_matrix[i][j] = max(prev_res, new_res)

    return total_matrix

def find_items(total_matrix):
    pass

def main():

    table = do_table(mass, weights, costs)

    print(table)
    print(table[-1][-1])


main()
