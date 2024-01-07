import json
import s3_db_files
from scanner_api import Scanner


def main():
    print('Starting...')
    jobs = s3_db_files.get_db_file('jobs.json', create=False)
    for job in jobs:
        if job['enabled'] is False:
            continue
        scanner = Scanner(job, test_mode=False)
        scanner.scan()


if __name__ == '__main__':
    main()
