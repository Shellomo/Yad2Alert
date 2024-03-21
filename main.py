import json
import os

import s3_db_files
from scanner_api import Scanner


def main(event, lambda_context):
    print('Starting...')

    # change working directory to /tmp
    print('Changing working directory to /tmp')
    os.chdir('/tmp')

    print(f'Getting jobs from s3 ({s3_db_files.bucket_name}/jobs.json)')
    jobs = s3_db_files.get_db_file('jobs.json', create=False)
    for job in jobs:
        if job['enabled'] is False:
            continue
        scanner = Scanner(job, test_mode=False)
        scanner.scan()


if __name__ == '__main__':
    main(0, 0)
