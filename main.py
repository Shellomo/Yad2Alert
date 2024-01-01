import json
from scanner_api import Scanner


def main():
    print('Starting scanner')
    with open('jobs.json', 'r') as f:
        jobs = json.load(f)
    for job in jobs:
        if job['enabled'] is False:
            continue
        scanner = Scanner(job, test_mode=False)
        scanner.scan()


if __name__ == '__main__':
    main()
