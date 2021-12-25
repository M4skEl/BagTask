import math
import sys


class BackpackTask:

    def __init__(self, mass=None, weights=[], costs=[], obj=[]):
        self.mass = mass
        self.weights = weights  # веса прдметов
        self.costs = costs  # стоимость предметов
        self.obj_list = obj  # индексы взятых предметов
        self.total_matrix = None
        self.price = 0
        self.nod = 0

    def calc_nod(self):
        self.nod = math.gcd(self.mass, self.weights[0])
        for elem in self.weights:
            self.nod = math.gcd(self.nod, elem)
        return int(self.nod)

    def do_table(self):
        if not self.mass:
            for i in range(len(self.weights)):
                if self.weights[i] == 0:
                    self.obj_list.append(i + 1)
                    self.price += self.costs[i]
            return

        self.nod = self.calc_nod()
        self.mass = int(self.mass / self.nod)
        for i in range(len(self.weights)):
            self.weights[i] = int(self.weights[i] / self.nod)

        self.total_matrix = [[0 for _ in range(self.mass + 1)] for __ in range(len(self.weights) + 1)]

        for i in range(len(self.weights) + 1):
            for j in range(self.mass + 1):

                if i == 0 or j == 0:
                    self.total_matrix[i][j] = 0
                    if j == 0:
                        if self.weights[i - 1] == 0:
                            self.total_matrix[i][j] = self.costs[i - 1]
                    continue
                if self.weights[i - 1] > j:
                    self.total_matrix[i][j] = self.total_matrix[i - 1][j]
                    continue
                prev_res = self.total_matrix[i - 1][j]
                new_res = self.costs[i - 1] + self.total_matrix[i - 1][j - self.weights[i - 1]]
                self.total_matrix[i][j] = max(prev_res, new_res)

        return self.total_matrix

    def find_items(self, i, j):
        if self.total_matrix[i][j] == 0:
            return
        if self.total_matrix[i - 1][j] == self.total_matrix[i][j]:
            self.find_items(i - 1, j)
        else:
            self.find_items(i - 1, j - self.weights[i - 1])
            self.obj_list.append(i)

    def total_calculate(self):
        self.total_matrix = self.do_table()
        if self.mass:
            self.find_items(len(self.total_matrix) - 1, len(self.total_matrix[0]) - 1)

    def print_answer(self, out):
        sum_mass = 0
        for iter in self.obj_list:
            if iter == 0:
                continue
            sum_mass += self.weights[iter - 1]

        if not self.mass:
            str_ans = str(sum_mass) + ' ' + str(self.price)
        else:
            str_ans = str(sum_mass * self.nod) + ' ' + str(self.total_matrix[-1][-1])

        print(str_ans, file=out)
        for elem in self.obj_list:
            print(elem, file=out)


def main():
    table = BackpackTask()

    for line in sys.stdin:
        line = line.rstrip('\r\n')

        if len(line.split()) == 1 and table.mass is None:
            table.mass = int(line.split()[0])
            continue

        elif len(line.split()) == 2 and table.mass is not None:
            if line.split()[0].isdigit() and line.split()[1].isdigit():
                table.weights.append(int(line.split()[0]))
                table.costs.append(int(line.split()[1]))
            else:
                print("error", file=sys.stdout)

        elif line == "end":
            break

        elif not (line and line.strip()):
            continue
        else:
            print("error", file=sys.stdout)

    table.total_calculate()
    table.print_answer(sys.stdout)


main()
