import os, re
import matplotlib.pyplot as plt

base_path = "logs_with_val"
all_logs = sorted(os.listdir(base_path))
fig, ax = plt.subplots(figsize=[10, 6])
color = ['b', 'g', 'r', 'c']
counter = 0

for file in all_logs:
    file_path = os.path.join(base_path, file)
    all_paths = []
    paths_obj_1 = []
    paths_obj_2 = []
    all_accuracies = []
    accuracies_obj_1 = []
    accuracies_obj_2 = []

    # print(file_path)
    with open(file_path, 'r') as log_file:
        all_lines = [line.strip() for line in log_file.readlines()]
        regex_string = "{*}|/step -"
        relevant_lines = [line for line in all_lines if re.search(regex_string, line)]
        for index in range(len(relevant_lines)):
            if index == len(relevant_lines)-1 or re.search("{*}", relevant_lines[index+1]):
                parsed_line = relevant_lines[index].split(' - ')[-3:-2]
                parsed_accuracy = parsed_line[0].split(': ')
                if obj_1:
                    accuracies_obj_1.append(float(parsed_accuracy[1]))
                else:
                    accuracies_obj_2.append(float(parsed_accuracy[1]))
                all_accuracies.append(float(parsed_accuracy[1]))
            if re.search("{*}", relevant_lines[index]):
                if file == 'val_accuracy_G0.txt':
                    obj_1_vertices = [1, 3, 4]
                    path_sort = relevant_lines[index].split(', ')
                    path_sort = path_sort[0].split('"')
                    if int(path_sort[-2]) in obj_1_vertices:
                        obj_1 = True
                        paths_obj_1.append(relevant_lines[index])
                    else:
                        obj_1 = False
                        paths_obj_2.append(relevant_lines[index])
                if file == 'val_accuracy_G1.txt':
                    obj_1_vertices = [1, 4, 5, 7, 9, 10]
                    path_sort = relevant_lines[index].split(', ')
                    path_sort = path_sort[0].split('"')
                    if int(path_sort[-2]) in obj_1_vertices:
                        obj_1 = True
                        paths_obj_1.append(relevant_lines[index])
                    else:
                        obj_1 = False
                        paths_obj_2.append(relevant_lines[index])
                if file == 'val_accuracy_G2.txt':
                    obj_1_vertices = [1, 3, 5]
                    path_sort = relevant_lines[index].split(', ')
                    path_sort = path_sort[0].split('"')
                    if int(path_sort[-2]) in obj_1_vertices:
                        obj_1 = True
                        paths_obj_1.append(relevant_lines[index])
                    else:
                        obj_1 = False
                        paths_obj_2.append(relevant_lines[index])
                if file == 'val_accuracy_G3.txt':
                    obj_1_vertices = [1, 3, 4, 5]
                    path_sort = relevant_lines[index].split(', ')
                    path_sort = path_sort[0].split('"')
                    if int(path_sort[-2]) in obj_1_vertices:
                        obj_1 = True
                        paths_obj_1.append(relevant_lines[index])
                    else:
                        obj_1 = False
                        paths_obj_2.append(relevant_lines[index])
                all_paths.append(relevant_lines[index])
    
        max_obj1 = max(accuracies_obj_1)
        max_obj2 = max(accuracies_obj_2)

        # print(max_obj1, max_obj2)

        index1 = all_accuracies.index(max_obj1)
        index2 = all_accuracies.index(max_obj2)

        objective_1_start = all_paths[index1]
        objective_1_end = all_paths[index1+1]

        objective_2_start = all_paths[index2]
        objective_2_end = all_paths[index2+1]

        index_line_start1 = relevant_lines.index(objective_1_start)
        index_line_end1 = relevant_lines.index(objective_1_end)

        index_line_start2 = relevant_lines.index(objective_2_start)
        index_line_end2 = relevant_lines.index(objective_2_end)

        values_obj1 = relevant_lines[index_line_start1+1:index_line_end1]
        values_obj2 = relevant_lines[index_line_start2+1:index_line_end2]

        include_false1 = objective_1_start.split('"train": ')
        include_false2 = objective_2_start.split('"train": ')

        y_values_1 = []
        index_false = 2
        iterator_value = 1
        last_value = None
        for line in values_obj1:
            parsed_line = line.split(' - ')[-3:-2]
            parsed_accuracy = parsed_line[0].split(': ')
            y_values_1.append(float(parsed_accuracy[1]))
            last_value = float(parsed_accuracy[1])
            if iterator_value % 5 == 0:
                if index_false < len(include_false1) and 'false' in include_false1[index_false]:
                    # print(include_false1[index_false], iterator_value)
                    y_values_1.append(last_value)
                index_false += 1
            iterator_value += 1

        # print(y_values_1)
        
        x1_version1 = [i for i in range(1, len(y_values_1)+1)]

        # print()
        y_values_2 = []
        index_false = 2
        iterator_value = 1
        last_value = None
        for line in values_obj2:
            parsed_line = line.split(' - ')[-3:-2]
            parsed_accuracy = parsed_line[0].split(': ')
            y_values_2.append(float(parsed_accuracy[1]))
            last_value = float(parsed_accuracy[1])
            if iterator_value % 5 == 0:
                if index_false < len(include_false2) and 'false' in include_false2[index_false]:
                    # print(include_false2[index_false], iterator_value)
                    y_values_2.append(last_value)
                index_false += 1
            iterator_value += 1
        
        x2_version1 = [i for i in range(1, len(y_values_2)+1)]
        # print(y_values_2)

        label_name = file[file.index('G'):file.index('G')+2]
        # ax.plot(x1_version1, y_values_1, color[counter], label= label_name + ' Objective 1')
        ax.plot(x2_version1, y_values_2, color[counter], label= label_name + ' Objective 2')
        counter += 1
    log_file.close()

ax.set_xticks([i for i in range(1,21)])
plt.xlabel('Number of steps')
plt.ylabel('Accuracy')
plt.legend(loc="lower right", prop={'size': 7})
plt.savefig('./diagrams/objective_2_low_lr.svg', format='svg', dpi=500)
