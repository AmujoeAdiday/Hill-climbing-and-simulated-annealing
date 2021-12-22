import random
import copy
import math
import sys


num_board_generated_Hill_climbing = 0
list_store_board = []
list_store_simm_search = []
num_cost_search_simm = 0


def board_generator(n):
    return [[random.randrange(0, 8) for i in range(8)] for x in range(n)]


def find_successor(current_state):
    # print("-----------------------------\nFrom find successor def")
    count_board_generated = 0
    min_val = 10000000
    # the board to update current board inside the loop
    min_board = current_state
    current = copy.deepcopy(current_state)
    # set the value to be higher than possible col and column [0,7] So, 10 is fine
    min_row = 10
    min_col = 10
    for i in range(len(current)):

        # store the value for the future that we will put it back
        initial_val = current[i]

        for j in range(len(current)):

            if j == initial_val:
                continue
            current[i] = j
            board_x = current
            count_board_generated += 1
            # print(board_x)

            # heuristic part
            hrt = heuristic(board_x)

            if hrt < min_val:
                # update min_val to its current heuristic (hrt)
                # also update the board>> state
                min_val = hrt
                # print("Found small value that is ", min_val)

                # modify the board
                min_col = i
                min_row = j

                # It won't update outside the loop from inside
                # print("Found better board that is ", min_board)

        # take the original value back in order to keep certain column in the same position while we move to work
        # on another column
        current[i] = initial_val

    # replace the min_row (j) in the current state in position the min of min_col
    current[min_col] = min_row

    # print("Found better board that is ", current)

    return current


def horizontal_attack(state):
    count_total = 0
    for i in range(len(state)):
        num = state[i]

        c = state[i + 1:].count(num)
        count_total += c
        # print("After removing",num," is ",c, "Total_total",count_total)
    return count_total


def diagonal_attack(state):
    pairs = []
    for col in range(len(state)):
        pairs.append((state[col], col))
    # print(pairs)

    count_match_right_down = 0
    count_match_right_up = 0
    for n in range(len(pairs)):

        target = pairs[0]
        # print("Target is ", target)
        pairs.remove(target)

        # print("pairs from removing", pairs)

        for j in range(len(pairs)):
            total_cost = target[0] + target[1]
            subtract_cost = target[0] - target[1]

            # right_down >> each(value.row+value.col) = target(value.row+value.col) --> valid
            if pairs[j][0] + pairs[j][1] == total_cost:
                count_match_right_down += 1

            # right_up >> each(value.row-value.col) = target(value.row-value.col) --> valid
            if pairs[j][0] - pairs[j][1] == subtract_cost:
                count_match_right_up += 1
        diagonal_count = count_match_right_down + count_match_right_up
        # print("count_match_right_down count_match_right_up diagonal_count", count_match_right_down,count_match_right_up,diagonal_count)

    diagonal_count = count_match_right_down + count_match_right_up
    # print("count_match_right_down count_match_right_up diagonal_count", count_match_right_down, count_match_right_up,diagonal_count)
    return diagonal_count


def heuristic(state):
    return horizontal_attack(state) + diagonal_attack(state)


def hill_climbing(initial):
    global num_board_generated_Hill_climbing
    global list_store_board
    current_b = initial

    num_board = 0
    success_count = 0

    while True:

        neighbor = find_successor(current_b)
        num_board += 56

        if heuristic(neighbor) >= heuristic(current_b):
            return current_b

        current_b = neighbor

        # print("Board generated is ", num_board)
        if heuristic(current_b) == 0:
            success_count += 1

        list_store_board.append(num_board)


def evaualte_fail_success(all_output_updated_current):
    num = 0
    percent = 0
    for i in all_output_updated_current:
        if heuristic(i) == 0:
            num += 1
    percent += num / len(all_output_updated_current)
    percent *= 100
    return [percent, num]


def run_hill_climbing(x):
    times = 0
    lis = board_generator(x)
    list_lastest_current_state = []

    while len(lis) > 0:
        times += 1
        # print("Random board is ", lis)
        # print("Times ", times)
        cur = hill_climbing(lis[0])
        list_lastest_current_state.append(cur)

        lis.remove(lis[0])
        # print("After removing is ",lis)
    # print(list_lastest_current_state)
    print("Hill-Climbing :", round(evaualte_fail_success(list_lastest_current_state)[0]), "% Average cost search",
          cost_search_hill_Climbing(list_store_board))


def cost_search_hill_Climbing(list_of_each_run_num_board):
    sum = list_of_each_run_num_board[len(list_of_each_run_num_board) - 1]

    # print(sum)
    index_list = []
    for i in range(len(list_of_each_run_num_board)):
        if list_of_each_run_num_board[i] == 56:
            index_list.append(i)
    # print(index_list)
    len_index_56 = len(index_list)

    index_list.remove(index_list[0])
    # print(index_list)
    for i in range(len(index_list)):
        index_list[i] -= 1
    # print(index_list)

    for i in range(len(list_of_each_run_num_board)):
        if i in index_list:
            sum += list_of_each_run_num_board[i]

    avg = sum / len_index_56
    return avg


def randomly_get_successor(current_state):
    # print("-----------------------------\nFrom find successor def")
    current = copy.deepcopy(current_state)
    list_of_all_successor = []
    for i in range(len(current)):
        # store the value for the future that we will put it back
        initial_val = current[i]
        for j in range(len(current)):
            if j == initial_val:
                continue
            current[i] = j
            board_x = copy.deepcopy(current)
            # print(board_x)
            list_of_all_successor.append(board_x)
        current[i] = initial_val
    return random.choice(list_of_all_successor)


def coolDown(T):
    return T * 0.99


def simulated_annealing(initial):
    global num_cost_search_simm
    current = copy.deepcopy(initial)
    # print("Initial state is ", current,"H is ", heuristic(current))

    T = 1000
    # print("T initially is ", T)
    t = 1
    success_fail_list = []
    track_time = 0
    count_success_run = 0
    count_unsuccessful_run = 0
    while heuristic(current) != 0:
        T = coolDown(T)
        track_time += 1

        if T < 0.0001:
            return current

        next_state = randomly_get_successor(current)

        diff_E = heuristic(next_state) - heuristic(current)

        if diff_E < 0:
            current = next_state
            # print("Found better state >> change to neighbor")

        else:

            ex = math.exp((-diff_E) / T)
            rand = random.uniform(0, 1)
            # print("EXPO : random is ", ex, rand)
            if ex > rand:
                # print("EXP is greater than rand")
                current = next_state
                # print("Didn't Found better state ")

        t += 1
    # print(t)

    # success_fail_list.append((1,t))
    num_cost_search_simm += t

    return success_fail_list


# for Annealing
def calculate_avg_run(run_list):
    avg_completed_run = 0
    avg_failed_run = 0
    percent_achieved = 0

    for i in range(len(run_list)):
        avg_failed_run += run_list[i][0]
        avg_completed_run += run_list[i][1]
    avg_failed_run = avg_failed_run / len(run_list)
    avg_completed_run = avg_completed_run / len(run_list)

    percent_achieved += (avg_completed_run / (avg_failed_run + avg_completed_run)) * 100
    return round(avg_failed_run), round(avg_completed_run), round(percent_achieved)


def run_simumated_annealing(x):
    global list_store_simm_search

    times = 0
    lis = board_generator(x)
    len_lis = len(lis)
    list_lastest_current_state = []

    while len(lis) > 0:
        times += 1
        # print("Random board is ", lis)
        # print("Times ", times)
        cur = simulated_annealing(lis[0])
        list_lastest_current_state.append(cur)

        lis.remove(lis[0])
        # print("After removing is ",lis)

    print("Simm. Annealing :", round(evaualte_fail_success(list_lastest_current_state)[0]), "% Average cost search",
          num_cost_search_Simm())

    # print("Result of both runs is fail VS completed VS percent achieved ",calculate_avg_run(lis_of_num_run))


def num_cost_search_Simm():
    return round(num_cost_search_simm / num)


def display_project():
    print(num, "puzzles")
    run_hill_climbing(num)
    # print("Average cost search",cost_search_hill_Climbing(list_store_board))
    run_simumated_annealing(num)
    # print("Average cost search", num_cost_search_Simm())

num = int(input("Type the number of random boards to be generated >>"))
display_project()









