import re
from pplint.model.Location import Location
from pplint.model.Problem import Problem
from pplint.model.Problem import ProblemLevel

class RACRule:
    parameters = None
    resulter = None
    warnings = []

    def __init__(self, parameters, resulter):
        self.parameters = parameters
        self.resulter = resulter

    def analyze(self):
        if len(self.parameters.diffs) > 0:
            for file_name in self.parameters.diffs:
                lines = self.parameters.diffs[file_name]
                index = 0
                for line in open(file_name, 'r').readlines():
                    index += 1
                    if index in lines:
                        if self.not_release_subject(line, file_name):
                            check_str = "检测到RACSubject实例可能未释放，检测有误请联系liudeping@bytedance.com"
                            location = Location(file_name, index, index)
                            problem = Problem("analyze_rac", ProblemLevel.WARNING, check_str, line, location)
                            self.warnings.append(problem.encode())
        if len(self.warnings) != 0:
            print("LocalLint analyze subject release failed, please check the html")

    def output(self):
        if len(self.warnings) != 0:
            self.resulter.add_result("analyze_subject", self.warnings)


    def not_release_subject(self, line, file_path):
        result = re.search('RACSubject *', line)
        other_result = re.search('RACSubject*', line)
        subject_name = ''
        if result != None or other_result != None:
            # 去除空格更好匹配
            replace_line = line.replace(" ", "")
            print(replace_line)
            matchObj = re.match(r'(.*)RACSubject\*(.*?);', replace_line, re.M | re.I)
            if matchObj:
                subject_name = matchObj.group(2)

        if len(subject_name) > 0:
            not_release = True
            release_str = subject_name + ' sendCompleted'
            print(release_str)
            for read_line in open(file_path, 'r').readlines():
                match_result = re.search(release_str, read_line)
                if match_result != None:
                    not_release = False
                    break
            return not_release
        else:
            return False

