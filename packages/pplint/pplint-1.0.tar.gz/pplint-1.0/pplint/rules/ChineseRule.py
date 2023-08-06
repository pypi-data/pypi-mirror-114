
from pplint.model.Location import Location
from pplint.model.Problem import Problem
from pplint.model.Problem import ProblemLevel

class ChineseRule:
    errors = []
    paramsters = None
    resulter = None

    def __init__(self, parameters, resulter):
        self.paramsters = parameters
        self.resulter = resulter

    def analyze(self):
        if len(self.paramsters.diffs) > 0:
            for file_name in self.paramsters.diffs:
                lines = self.paramsters.diffs[file_name]
                index = 0
                for line in open(file_name, 'r').readlines():
                    index += 1
                    if index in lines:
                        if self.contains_chinese(line):
                            check_str = "检测到有中文，请替换为英文，检测有误请联系liudeping@bytedance.com"
                            location = Location(file_name, index, index)
                            problem = Problem("analyze_chinese", ProblemLevel.ERROR , check_str, line, location)
                            self.errors.append(problem.encode())
        if len(self.errors) != 0:
            print("LocalLint analyze chinese failed, please check the html")

    def output(self):
        if len(self.errors) != 0:
            self.resulter.add_result("analyze_chinese", self.errors)

    def contains_chinese(self, line):
        def character_is_chinese(character):
            result = ord(character)
            if result == ':':
                pass
            t = result in range(0x4E00, 0x9FA5)
            return t
        for character in line:
            if character_is_chinese(character):
                return True
        return False