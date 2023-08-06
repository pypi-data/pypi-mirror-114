import sys
import os

def exit_success(paramters):
    if os.path.exists(paramters.project_path):
        commit_ids_path = os.path.join(paramters.project_path, ".git/hooks/ids.txt")
        if os.path.isfile(commit_ids_path):
            commit_ids = open(commit_ids_path).read().split('\n')[:-1]
            new_commit_ids = []
            for commit_id in commit_ids:
                if commit_id not in paramters.hit_commit_ids:
                    new_commit_ids.append(commit_id)
            with open(commit_ids_path, 'w') as f:
                for commit_id in new_commit_ids:
                    f.write(commit_id+'\n')
    sys.exit()

def exit_end(paramters):
    try:
        sys.stdin = open('/dev/tty', 'r')
        a = input("-----LocalLint-----> Do you want to ignore the issues and push the code? (y / n): ")
        if a.lower() == 'y':
            exit_success(paramters)
        else:
            sys.exit(1)
    except Exception as e:
        sys.exit(1)