import uuid
from os import path
from git import Repo
import os

main_curr_dir = os.path.dirname(os.path.realpath(__file__)).replace('github_bot_file_commit', '')
main_repo = Repo(main_curr_dir)
repo = Repo.clone(main_repo, 'repo_copy')
curr_dir = repo.git_dir.replace('.git', '')
print(1)

def commit_files(new_branch, file, f_name):
    if repo is None:
        return False

    current = main_repo.create_head(new_branch)
    current.checkout()
    master = main_repo.heads.master
    main_repo.git.pull('origin', master)

    # creating file
    with open(curr_dir + path.sep + f_name, 'w') as new:
        new.write(file.read().decode())
    if not path.exists(curr_dir):
        os.makedirs(curr_dir)
    print('file created---------------------')

    if repo.index.diff(None) or repo.untracked_files:

        repo.git.add(A=True)
        repo.git.commit(m='msg')
        repo.git.push('--set-upstream', 'origin', current)
        print('git push')
    else:
        print('no changes')


if __name__ == '__main__':
    with open('client_branch.py', 'rb') as f:
        name = str(uuid.uuid4())
        commit_files(name, f, 'test_file.py')
        print(name)
