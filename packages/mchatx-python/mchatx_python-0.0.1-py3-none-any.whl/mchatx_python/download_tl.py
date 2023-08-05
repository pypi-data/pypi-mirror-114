import argparse
import mchatx_python.api as api
import json
from functools import partial

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('room_link', nargs='?', help='The room link of the MChad archive you want to download')
    args = parser.parse_args()
    return args

def download_archive(mc, room):
    with open(f'{room}.json', 'w') as archive_output:
        data = mc.download_archive(room)
        json.dump(data, archive_output)
        print(f'Wrote {room}.json')


def main():
    args = get_args()
    mc = api.MChatX()

    rooms = [args.room_link]
    if not args.room_link:
        archives = mc.get_archive_list()

        print("{:4} {:20} {:30}".format('id', 'room/user', 'room name'))
        for i, archive in enumerate(archives):
            print(f"{i:<4} {archive['Room']:20} {archive['Nick']:30}")
        print('\n')
        print("Please enter the ids of the archives you'd like to download, separated by ','")
        string = input("ids (ex. 1,2,9): ")
        values = list(map(lambda s: int(s.strip()), string.split(',')))
        print(values)
        rooms = list(map(lambda i: archives[i]['Link'], values))
    print(rooms)

    for room in rooms:
        download_archive(mc, room)

if __name__ == '__main__':
    main()
