import os
import json
import requests
import stat

from pplint.util.fileUtil import get_project_path

HOOK_URL_DICTIONARY = {
    'post-commit': "https://code.byted.org/ugc/LocalLint/raw/dev/githook/post-commit",
    'commit-msg': "https://code.byted.org/ugc/LocalLint/raw/dev/githook/commit-msg",
    'pre-push': "https://code.byted.org/ugc/LocalLint/raw/dev/githook/pre-push"
}

class Init():
    def __init__(self):
        repo_path = get_project_path()
        git_dir = os.path.join(repo_path, '.git')
        hook_dir = os.path.join(repo_path, '.git', 'hooks')
        if os.path.isdir(git_dir):
            if not os.path.exists(hook_dir):
                os.mkdir(hook_dir)
        #init post-commit
        self.config_hook_files(hook_dir, 'post-commit')
        ids_path = os.path.join(hook_dir, 'ids.txt')
        if not os.path.isfile(ids_path):
            f = open(ids_path, 'w')
            f.close()

        #init commit-msg
        self.config_hook_files(hook_dir, 'commit-msg')
        #init pre-push
        self.config_hook_files(hook_dir, 'pre-push')

    def download_file(self, file_name, hook_path):
        url = HOOK_URL_DICTIONARY[file_name]
        if not os.path.exists(hook_path):
            print(url)
            rsp = requests.get(url, headers={'Private-Token': 'dy_5ZxKo9JDezsyiYxPM'})
            with open(hook_path, 'wb') as hook:
                 hook.write(rsp.content)
                 hook.flush()
            os.chmod(hook_path, stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)

    def config_hook_files(self, dir, file_name):
        hook_path = os.path.join(dir, file_name)
        if not os.path.exists(hook_path):
            self.download_file(file_name, hook_path)