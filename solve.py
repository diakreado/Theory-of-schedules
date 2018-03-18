import numpy as np
from read_graph import read_graph
from plot_diagram import plot_diagram


def print_result(all_done_works, available_works, chosen_works, done_works, end_moments, happened_events, matrix, t):
    print("---------------------")
    print("T:\n", t)
    print("aD:\n", all_done_works)
    print("D:\n", done_works)
    print("E:\n", happened_events)
    print("W:\n", available_works)
    print("A:\n", get_duration(available_works, matrix).transpose())
    print("V:\n", chosen_works)
    print("L:\n", end_moments)


def print_result_latex(available_works, chosen_works, done_works, end_moments, happened_events, matrix, t):
    result = str(t) + " & " + str(done_works.tolist() if isinstance(done_works, np.ndarray) else done_works) \
             + " & " + str(happened_events) + " & " + str(available_works.tolist()) \
             + " & " + str(get_duration(available_works, matrix).transpose().tolist()) + " & " \
             + str(chosen_works.tolist()) + " & " + str(end_moments.tolist()) + " \\\\ \hline "

    result = result.replace("[[", "[")
    result = result.replace("]]", "]")
    result = result.replace("[]", "[~]")
    result = result.replace(",", "")
    result = result.replace(".0", "")

    print(result)


def get_duration(works, matrix):
    duration = []
    for work in works:
        duration.append(int(matrix[work[0]][work[1]]))
    return np.array(duration)


def get_available_works(matrix, events, done_works):
    works = []
    for start_event in events:
        for end_event in range(len(matrix[start_event])):
            if matrix[start_event][end_event] != '-':
                work = [start_event, end_event]
                if work not in done_works.tolist():
                    works.append(work)
    return np.array(works)


def get_available_events(matrix, done_works):
    events = []
    for current_event in range(len(matrix)):
        previous_events = []
        for previous_event in range(len(matrix)):
            if matrix[previous_event][current_event] != '-':
                previous_events.append(previous_event)
        works = np.array(list(filter(lambda x: x[1] == current_event and x[0] in previous_events, done_works)))
        if len(works) == len(previous_events):
            events.append(current_event)
    return np.array(events)


def get_reserve_time(works, matrix):
    reserve_time = []
    for work in works:
        reserve_time.append(int(matrix[work[0]][work[1]]))
    return np.array(reserve_time)


def choose_works(matrix, available_works, reserve_time_matrix, workers_number, type=0):
    duration = get_duration(available_works, matrix)
    reserve_time = get_reserve_time(available_works, reserve_time_matrix)

    work_array = duration
    multiplier = -1

    if type == 1:
        multiplier = 1
    elif type == 2:
        work_array = reserve_time
    elif type == 3:
        work_array = reserve_time
        multiplier = 1

    sorted_indecies = sorted(range(len(work_array)), key=lambda k: multiplier * work_array[k])
    while workers_number < len(sorted_indecies):
        sorted_indecies.pop()
    chosen_works = []
    for i in sorted_indecies:
        chosen_works.append(available_works[i])
    return np.array(chosen_works)


def solve(matrix, reserve_time, workers_number, type=0):

    all_time = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j].isnumeric():
                all_time += float(matrix[i][j])

    print("All time:", all_time)

    t = 0
    all_done_works = np.array([])
    happened_events = np.array([0])
    done_works = []

    available_works = get_available_works(matrix, happened_events, all_done_works)
    chosen_works = choose_works(matrix, available_works, reserve_time, workers_number, type)
    end_moments = get_duration(chosen_works, matrix) + t

    t_story = [t]
    works_story = [chosen_works]

    print_result_latex(available_works, chosen_works, done_works, end_moments, happened_events, matrix, t)

    while len(happened_events) != len(matrix):

        dt = np.min(end_moments)
        t += dt

        done_mask = end_moments == dt
        done_works = chosen_works[done_mask]
        all_done_works = done_works if len(all_done_works) == 0 \
            else np.append(all_done_works, done_works, axis=0)

        chosen_works = chosen_works[np.invert(done_mask)]
        happened_events = get_available_events(matrix, all_done_works)
        available_works = get_available_works(matrix, happened_events, np.append(all_done_works, chosen_works, axis=0))
        new_works = choose_works(matrix, available_works, reserve_time, workers_number - len(chosen_works), type)
        chosen_works = chosen_works if len(new_works) == 0 else np.append(chosen_works, new_works, axis=0)
        end_moments = end_moments[np.invert(done_mask)] - dt
        end_moments = np.append(end_moments, get_duration(new_works, matrix))

        works_story.append(chosen_works)
        t_story.append(t)

        print_result_latex(available_works, chosen_works, done_works, end_moments, happened_events, matrix, t)

    plot_diagram(t_story, works_story, workers_number)




if __name__ == '__main__':
    matrix, early_moments, late_moments, reserve_time = read_graph('input_data', True)
    solve(np.array(matrix), np.array(reserve_time), 3, 3)
