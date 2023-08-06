import git
import os
import sys
import subprocess
from unidiff import PatchSet
from io import StringIO

def get_repo_tree(repo, sha, time):
    try:
        return repo.tree(sha + '^{tree}')
    except ValueError as e:
        os.system("git fetch --all")
        if time < 2:
            return get_repo_tree(repo, sha, time)
        else:
            return repo.tree(sha + '^{tree}')

def get_line_number(patch_file):
    added_line_numbers = []
    for code_lump in patch_file:
        for code_line in code_lump:
            if code_line.is_added and code_line.value.strip() != '':
                added_line_numbers.append(int(code_line.target_line_no))
    return added_line_numbers;

# 筛选属于作者提交的部分，去除掉其他同学提交的代码，比如说merge了其他分支的代码等case
def filter_author_files(repo_path, local_SHA, remote_SHA):
    repo = git.Repo(repo_path)
    author_name = repo.config_reader().get_value('user', 'name')
    curr_path = os.getcwd()
    os.chdir(repo_path)
    old_color_config = os.popen('git config --global color.diff').read()
    os.system('git config --global color.diff false')
    uni_diff_text = os.popen('git show -p {0}...{1} --author="{2}"'.format(local_SHA, remote_SHA, author_name)).read()
    os.system('git config --global color.diff ' + old_color_config)
    uni_diff_text = uni_diff_text.replace("\n\n", "\n").strip("\n")+"\n"
    os.chdir(curr_path)
    patch_set = PatchSet(StringIO(uni_diff_text))
    author_files = []
    for patch_file in patch_set:
        if patch_file.target_file != '/dev/null':
            file_name = patch_file.target_file[2:]
            file_path = os.path.join(repo_path, file_name)
            if file_path not in author_files:
                author_files.append(file_path)
    return author_files

def filter_blame(repo_path, change_list, new_added_files):
    repo = git.Repo(repo_path)
    curr_path = os.getcwd()
    os.chdir(repo_path)
    author_name = repo.config_reader().get_value('user', 'name')
    pop_file = []
    for change_file in change_list:
        if change_file in new_added_files:
            continue
        new_lines = []
        blames = get_file_blame(change_file)
        for line in change_list[change_file]:
            try:
                if blames[line-1].find(author_name) != -1:
                    new_lines.append(line)
            except:
                print("%s: get filter_blame failed" % change_file)
        if len(new_lines) > 0:
            change_list[change_file] = new_lines
        elif len(change_list[change_file]) == 0 and blames[0].find(author_name) != -1:
            change_list[change_file] = new_lines
        else:
            pop_file.append(change_file)
    for f in pop_file:
        change_list.pop(f)
    os.chdir(curr_path)

# blame file
def get_file_blame(file_path):
    blames = []
    cmd = 'git blame %s' % file_path
    with os.popen(cmd) as process:
        try:
            result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
            blames = result.stdout.decode().split('\n')
        except UnicodeDecodeError as e:
            result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
            blames = [result.stdout.split()[1].decode()]
    return blames

def get_diff_files(repo_path, local_SHA, remote_SHA):
    repo = git.Repo(repo_path)
    new_tree = get_repo_tree(repo, local_SHA, 1)
    old_tree = get_repo_tree(repo, remote_SHA, 1)
    old_color_config = os.popen('git config --global color.diff').read()
    os.system('git config --global color.diff false')
    uni_diff_text = repo.git.diff(old_tree, new_tree)
    os.system('git config --global color.diff ' + old_color_config)
    uni_diff_text = uni_diff_text.replace("\n\n", "\n").strip("\n")+"\n"
    author_files = filter_author_files(repo_path, local_SHA, remote_SHA)
    patch_set = PatchSet(StringIO(uni_diff_text))
    change_list = {}
    is_added_files = []
    for patch_file in patch_set:
        if patch_file.target_file != '/dev/null':
            file_name = patch_file.target_file[2:]
            file_path = os.path.join(repo_path, file_name)
            if file_path not in author_files:
                continue
            if file_path not in change_list:
                change_list[file_path] = []

            added_line_numbers = get_line_number(patch_file)
            change_list[file_path].extend(added_line_numbers)
            if patch_file.is_added_file:
                is_added_files.append(os.path.join(repo_path, file_name))
    filter_blame(repo_path, change_list, is_added_files)
    return change_list
