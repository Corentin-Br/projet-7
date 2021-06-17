import csv

import numpy as np

MAX_COST = 500


def read_csv_file(file_name):
    """Get the data from a csv file and return it as a list of dictionaries."""
    with open(f"{file_name}.csv", newline='') as file:
        csv_data = csv.reader(file)
        data = []
        for i, row in enumerate(csv_data):
            if i == 0:
                continue
            data.append({"name": row[0],
                         "cost": float(row[1]),
                         "profit": float(row[2])
                         })
    return data


def clean_data(data):
    """Return entries in data that can be used."""
    return [entry for entry in data if is_valid(entry)]


# def reduce_data(data, min_profit):
#     """Remove entries the profit of which is under a certain value"""
#     return [entry for entry in data if entry["profit"] >= min_profit]


def is_valid(entry):
    """Check if the profit and the cost of the entry are valid."""
    if MAX_COST < entry["cost"] or entry["cost"] <= 0 or entry["profit"] <= 0:
        return False
    return True


def increase_scale(data, max_cost):
    """Increase the order of magnitude of costs.

    The purpose of this function is to prepare for dynamic programming, by transforming all decimal values into
    integers."""
    for entry in data:
        entry["cost"] *= 10
    max_cost *= 10
    return data, max_cost


def solve_knapsack(data):
    """Use dynamic programming to solve the knapsack problem."""
    oom_increase = 1  # Represent the increase in order of magnitude.
    max_cost = MAX_COST
    for entry in data:
        while not format(entry["cost"], '.12g').isnumeric():
            data, max_cost = increase_scale(data, max_cost)
            oom_increase *= 10
        entry["cost"] = round(entry["cost"])
    solution_array = generate_solving_array(data, max_cost)
    solution_index, optimal_value, optimal_spending = get_solution_from_array(solution_array, data)
    solution = ", ".join([data[index]["name"] for index in solution_index])
    print(f"By buying {solution},")
    print(f"You'll spend {optimal_spending/oom_increase} and earn {round(optimal_value/oom_increase, 2)}")


# def solve_knapsack_greedy(data):
#     """Use a greedy algorithm to solve the knapsack problem.
#
#     It doesn't provide a perfect solution, it is only used to provide a minimum value for the profit of each item."""
#     data.sort(key=lambda element: element["profit"], reverse=True)
#     current_cost = 0
#     solution = []
#     for entry in data:
#         if entry["cost"] + current_cost < 500:
#             solution.append(entry)
#             current_cost += entry["cost"]
#     solution.sort(key=lambda element: element["profit"])
#     return solution[0]["profit"]


def generate_solving_array(data, max_cost):
    """
    Use dynamic programming to generate an array that contains the optimal value and can be used to determine how to
    reach said value."""
    row_number = len(data) + 1
    column_number = max_cost + 1
    array = np.empty((row_number, column_number))
    array[0] = np.zeros(column_number)
    for i in range(1, len(array)):
        cost = data[i - 1]["cost"]
        profit = data[i - 1]["cost"] * data[i - 1]["profit"] / 100
        for j in range(column_number):
            if j >= cost:
                array[i, j] = max(array[i - 1, j],
                                  array[i - 1, j - cost] + profit)
            else:
                array[i, j] = array[i - 1, j]
    return array


def get_solution_from_array(array, data):
    """Get the combination of actions providing the optimal value."""
    solution_index = []
    optimal_value = array[-1][-1]
    fitting_values = np.asarray(array == optimal_value).nonzero()  # Some kind of magical formula. asarray
    # gives an array of the same dimensions as the input, but with True or False, depending if they fulfill the
    # condition or not,  then nonzero() removes all values equal to 0 (here, False).
    initial_row_index = fitting_values[0][0]
    column_index = optimal_spending = fitting_values[1][0]
    for i in range(initial_row_index, -1, -1):
        cost = data[i - 1]["cost"]
        profit = data[i - 1]["cost"] * data[i - 1]["profit"] / 100
        if column_index >= cost:
            if array[i - 1, column_index - cost] + profit >= array[i - 1, column_index]:
                solution_index.append(i - 1)
                column_index -= cost
    return solution_index, optimal_value, optimal_spending


def main():
    keep_going = True
    while keep_going:
        file_name = input("What is the name of the csv file containing the data (do not include the extension)?")
        data = clean_data(read_csv_file(file_name))
        # minimum_profit = solve_knapsack_greedy(data)
        # data = reduce_data(data, minimum_profit)
        solve_knapsack(data)
        more = input("Do you want to solve another set of data? (y/n)")
        if more != "y":
            keep_going = False
            print("The program is closing")
    return


if __name__ == "__main__":
    main()
