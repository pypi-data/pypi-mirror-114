import getopt
import os
import subprocess

from pplint.util.fileUtil import get_project_path
from pplint.util.gitUtil import get_diff_files

class Parameters:
    source_branch = ""
    target_branch = ""
    remote_branch = ""
    local_SHA = ""
    remote_SHA = ""
    project_path = ""
    hook_type = ""
    commit_msg_path = ""
    commit_ids_path = ""
    output_path = ""
    hit_commit_ids = []
    diffs = {}
    def __init__(self, argv):
        self.project_path = get_project_path()
        os.chdir(self.project_path)
        self.commit_ids_path = os.path.join(self.project_path, ".git/hooks/ids.txt")
        self.output_path = os.path.join(self.project_path, '.git/build/reporter')
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)
        opts = self.analye_argv(argv)
        for opt, arg in opts:
            print(opt)
            print(arg)
            if opt == '--sourceBranch':
                self.source_branch = arg
            elif opt == '--targetBranch':
                self.target_branch = arg
            elif opt == '--localSHA':
                self.local_SHA = arg
            elif opt == '--remoteSHA':
                self.remote_SHA = arg
            elif opt == '--remoteBranch':
                self.remote_branch = arg
            elif opt == '--hookType':
                self.hook_type = arg
            elif opt == '--commitMsgPath':
                self.commit_msg_path = arg

    def analyze_diffs(self):
        diffs = {}
        if self.hook_type == "commit-msg" and self.commit_msg_path != "":
            commit_msg_path = os.path.join(self.project_path, self.commit_msg_path)
            commit_msg_lines = open(commit_msg_path).readline()
            diffs = {commit_msg_path: list(range(1, len(commit_msg_lines) + 1))}
        else:
            if os.path.exists(self.project_path):
                os.chdir(self.project_path)
                ids_path = os.path.join(self.project_path, ".git/hook/ids.txt")
                local_SHA = self.get_commit_id('HEAD', 0)
                remote_SHA = self.get_remote_sha()
                get_diff = get_diff_files(self.project_path, local_SHA, remote_SHA)
                diffs.update(get_diff)
        self.diffs = diffs

    def get_commit_id(self, commit_id, index):
        cmd = "git rev-parse %s~%s" % (commit_id, index)
        result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8").strip("\n")

    def get_remote_sha(self):
        initial_commit_id = "0000000000000000000000000000000000000000"
        if self.remote_SHA != initial_commit_id:
            return self.remote_SHA

        current_branch = self.get_commit_id('HEAD', 0)
        if not os.path.isfile(self.commit_ids_path):
            return current_branch
        commit_ids = open(self.commit_ids_path).read().split('\n')[:-1]
        current_branch, index = self.commit_id_valid(current_branch, commit_ids)

        while current_branch in commit_ids:
            self.hit_commit_ids.append(current_branch)
            index += 1
            current_branch = self.get_commit_id('HEAD', index)
            current_branch, temp_index = self.commit_id_valid(current_branch, commit_ids)
            index += temp_index
        return current_branch


    def commit_id_valid(self, current_commit_id, ids):
        index = 0
        order_commit_id = current_commit_id
        if current_commit_id not in ids:
            while index < 3:
                index += 1
                current_commit_id = self.get_commit_id(current_commit_id, 1)
                if current_commit_id in ids:
                    order_commit_id = current_commit_id
                    break
        return order_commit_id, index

    def analye_argv(self, argv):
        opts, args = getopt.getopt(argv[1:], '', ["analyze", "hookType=", "localSHA=", "remoteSHA=", "projectPath=", "remoteBranch", "commitMsgPath="])
        return opts