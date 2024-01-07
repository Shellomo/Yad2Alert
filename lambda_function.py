import os
import subprocess
import sys

REPO_URL = 'https://github.com/Shellomo/Yad2Alert'
REPO_NAME = REPO_URL.split('/')[-1]  # Extracts the repository name from the URL


def clone_repo():
    subprocess.run(['git', 'clone', REPO_URL])


def install_requirements():
    # Ensure the requirements file is in the cloned repository
    requirements_path = os.path.join(REPO_NAME, 'requirements.txt')
    # pip install custom package to /tmp/ and add to path
    subprocess.call(f'pip3 install -r {requirements_path} -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    sys.path.insert(1, '/tmp/')


def lambda_handler(event, context):
    print('Starting...')

    # change directory to /tmp
    os.chdir('/tmp')

    clone_repo()
    print(f'Cloned repository: {REPO_NAME}')

    # Change directory to the cloned repository
    os.chdir(REPO_NAME)
    print(f'Changed directory to: {REPO_NAME}')

    install_requirements()
    print('Installed requirements')

    # Run the main script. Make sure 'main.py' is in the root of the cloned repository
    os.system('python3 main.py')


# Add a conditional to prevent execution when imported as a module
if __name__ == "__main__":
    lambda_handler(None, None)
