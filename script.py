with open('input_data') as input_file:
    input_matrix = [row.strip() for row in input_file]
SIZE_OF_INPUT_MATRIX = input_matrix.__len__()

early_moments = [0 for i in range(SIZE_OF_INPUT_MATRIX)]
for i in range(1, SIZE_OF_INPUT_MATRIX):
    max_value_for_moment = 0
    for j in range(SIZE_OF_INPUT_MATRIX):
        if input_matrix[j][i] != '-':
            value_of_way_to_point = early_moments[j] + int(input_matrix[j][i])
            if value_of_way_to_point > max_value_for_moment:
                max_value_for_moment = value_of_way_to_point
    early_moments[i] = max_value_for_moment

SIZE_OF_CRITICAL_WAY = early_moments[SIZE_OF_INPUT_MATRIX-1]

late_moments = [SIZE_OF_CRITICAL_WAY for i in range(SIZE_OF_INPUT_MATRIX)]
for i in reversed(range(SIZE_OF_INPUT_MATRIX - 1)):
    min_value_for_moment = SIZE_OF_CRITICAL_WAY
    for j in range(SIZE_OF_INPUT_MATRIX):
        if input_matrix[i][j] != '-':
            value_of_way_to_point = late_moments[j] - int(input_matrix[i][j])
            if value_of_way_to_point < min_value_for_moment:
                min_value_for_moment = value_of_way_to_point
    late_moments[i] = min_value_for_moment

reserve_time = [[-1 for j in range(SIZE_OF_INPUT_MATRIX)] for i in range(SIZE_OF_INPUT_MATRIX)]
critical_way = '1'
for i in range(SIZE_OF_INPUT_MATRIX):
    for j in range(SIZE_OF_INPUT_MATRIX):
        if input_matrix[i][j] != '-':
            value_of_reserve = late_moments[j] - early_moments[i] - int(input_matrix[i][j])
            reserve_time[i][j] = value_of_reserve
            if value_of_reserve == 0:
                critical_way += '->' + str(j+1)

print(early_moments)
print(late_moments)
# print()
# for i in range(SIZE_OF_INPUT_MATRIX):
#     print(reserve_time[i])
# print()
print(critical_way)
