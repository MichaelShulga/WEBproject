import sys
from time import *
from os import path
from git import Repo
import os

print(os.path.basename(sys.path[1]))
curr_dir = os.path.dirname(os.path.realpath(__file__)).replace('github_bot_file_commit', '')
print(curr_dir)
repo = Repo(curr_dir)


def commit_files():
    if repo != None:
        new_branch = 'your_new_branch'
        current = repo.create_head(new_branch)
        current.checkout()
        master = repo.heads.master
        repo.git.pull('origin', master)
        # creating file
        dtime = strftime('%d-%m-%Y %H:%M:%S', localtime())
        with open(curr_dir + path.sep + 'lastCommit' + '.txt', 'w') as f:
            f.write(str(dtime))
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


commit_files()
