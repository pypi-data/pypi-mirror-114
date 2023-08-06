import sys
import os
import csv
import json


def progres_bar(total, progress, status=''):
    # Displays or updates a console progress bar.
    # Original source: https://stackoverflow.com/a/15860757/1391441

    barLength = 20
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "#" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()


def file_colision_detector(file_name, extra_path):
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_name = file_name.split('.')

    if extra_path != '':
        path = f'{path}/{extra_path}'
        if not os.path.isdir(f'{path}/'):
            os.mkdir(path)

    if os.path.isfile(f'{path}/{file_name[0]}-(0).{file_name[1]}'):
        i = 1
        while os.path.isfile(f'{path}/{file_name[0]}-({i}).{file_name[1]}'):
            i += 1
        return f'{path}/{file_name[0]}-({i}).{file_name[1]}'
    else:
        return f'{path}/{file_name[0]}-(0).{file_name[1]}'


def save_list_of_dicts_to_csv(list_of_dicts, filename, path):
    if len(list_of_dicts) == 0:
        print('\nnothing to save in csv\n')
        return False
    filename = file_colision_detector(filename, path)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(list(list_of_dicts[0].keys()))

        for item in list_of_dicts:
            # remove empty lines
            if all([x == '' for x in list(item.values())]):
                continue
            wr.writerow(list(item.values()))

    print(f'\nFile is ready: {filename}\n')


def save_dict_to_json(dct, filename, path):
    filename = file_colision_detector(filename, path)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dct, f, ensure_ascii=False, indent=4)

    print(f'\nFile is ready: {filename}\n')
