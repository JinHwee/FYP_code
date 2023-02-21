import pandas as pd
import openpyxl, os

def read_text_files():
    cwd = os.getcwd()
    text_files = [x for x in os.listdir() if x.endswith('.txt')]

    all_data = {}
    for file in text_files:
        with open(file, 'r') as data_input:
            lines = [x.strip() for x in data_input.readlines()]
            lines = [x for x in lines if x]
            for id in range(0, len(lines), 2):
                data = lines[id+1].split(', ')
                for string in data:
                    information = string.split(': ')
                    tmp_dict = all_data.get(lines[id][:-1], {})
                    tmp_arr = tmp_dict.get(information[0], [])
                    tmp_arr.append(float(information[1]))
                    tmp_dict[information[0]] = tmp_arr
                    all_data[lines[id][:-1]] = tmp_dict
        data_input.close()
    
    row_index = [x for x in range(10, 501, 10)]
    n_plus_1 = []
    n = []
    n_add_1 = []
    n_plus_1_delete_1 = []
    for id in range(len(row_index)):
        tmp_dict = all_data[str(row_index[id])]
        for key, value in tmp_dict.items():
            if '(n+1)' in key:
                avg_value = sum(value) / len(value)
                n_plus_1.append(avg_value)
            if '(n)' in key:
                avg_value = sum(value) / len(value)
                n.append(avg_value)
            if 'Add' in key:
                avg_value = sum(value) / len(value)
                n_add_1.append(n[id] + avg_value) 
            if 'Delete' in key:
                avg_value = sum(value) / len(value)
                n_plus_1_delete_1.append(avg_value)

    df = pd.DataFrame([n_plus_1, n, n_add_1, n_plus_1_delete_1], columns=row_index, index=list(all_data['10'].keys()))
    df.to_excel('benchmark.xlsx', sheet_name='Diagrams')
    
read_text_files()
