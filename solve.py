import numpy as np
from read_graph import read_graph


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


def choose_works(matrix, available_works, reserve_time_matrix, workers_number):
    duration = get_duration(available_works, matrix)
    reserve_time = get_reserve_time(available_works, reserve_time_matrix)
    # print("\n", reserve_time, "\n")
    # print("\n", duration)
    # sorted_indecies = sorted(range(len(duration)), key=lambda k: duration[k])
    sorted_indecies = sorted(range(len(reserve_time)), key=lambda k: -reserve_time[k])
    # print(sorted_indecies)
    while workers_number < len(sorted_indecies):
        sorted_indecies.pop()
    # print(sorted_indecies, "\n")
    chosen_works = []
    for i in sorted_indecies:
        chosen_works.append(available_works[i])
    return np.array(chosen_works)


def solve(matrix, early_moments, late_moments, reserve_time, workers_number):

    t = 0
    all_done_works = np.array([])
    happened_events = np.array([0])
    done_works = []

    available_works = get_available_works(matrix, happened_events, all_done_works)
    chosen_works = choose_works(matrix, available_works, reserve_time, workers_number)
    end_moments = get_duration(chosen_works, matrix) + t

    # print("---------------------")
    # print("T:\n", t)
    # # print("aD:\n", all_done_works)
    # print("D:\n", done_works)
    # print("E:\n", happened_events)
    # print("W:\n", available_works)
    # print("A:\n", get_duration(available_works, matrix).transpose())
    # print("V:\n", chosen_works)
    # print("L:\n", end_moments)
    print(t, end=" & ")
    # print("aD:\n", all_done_works)
    print(done_works, end=" & ")
    print(happened_events, end=" & ")
    print(available_works, end=" & ")
    print(get_duration(available_works, matrix).transpose(), end=" & ")
    print(chosen_works, end=" & ")
    print(end_moments, end=" \\\\ \hline \n ")

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
        new_works = choose_works(matrix, available_works, reserve_time, workers_number - len(chosen_works))
        chosen_works = chosen_works if len(new_works) == 0 else np.append(chosen_works, new_works, axis=0)
        end_moments = end_moments[np.invert(done_mask)] - dt
        end_moments = np.append(end_moments, get_duration(new_works, matrix))

        # print("---------------------")
        # print("T:\n", t)
        # # print("aD:\n", all_done_works)
        # print("D:\n", done_works)
        # print("E:\n", happened_events)
        # print("W:\n", available_works)
        # print("A:\n", get_duration(available_works, matrix).transpose())
        # print("V:\n", chosen_works)
        # print("L:\n", end_moments)
        print(t, end=" & ")
        # print("aD:\n", all_done_works)
        print(done_works, end=" & ")
        print(happened_events, end=" & ")
        print(available_works, end=" & ")
        print(get_duration(available_works, matrix).transpose(), end=" & ")
        print(chosen_works, end=" & ")
        print(end_moments, end=" \\\\ \hline \n ")


if __name__ == '__main__':
    matrix, early_moments, late_moments, reserve_time = read_graph('input_data', True)
    solve(np.array(matrix), np.array(early_moments), np.array(late_moments), np.array(reserve_time), 2)
