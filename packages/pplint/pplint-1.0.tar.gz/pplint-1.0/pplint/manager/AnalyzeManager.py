import os
import threading

from pplint.util.sysUtil import exit_end
from pplint.output.Result import Result
from pplint.rules.ChineseRule import ChineseRule
from pplint.rules.RACRule import RACRule

class AnalyzeManager:
    rules = []
    parameters = None
    result = None

    def __init__(self, paramters):
        self.paramters = paramters
        self.result = Result()
        chinese_rule = ChineseRule(paramters, self.result)
        self.rules.append(chinese_rule)
        rac_rule = RACRule(paramters, self.result)
        self.rules.append(rac_rule)

    def start_analyze(self):
        try:
            project_path = self.paramters.project_path
            if os.path.exists(project_path):
                os.chdir(project_path)
                self.paramters.analyze_diffs()
                threads = {}
                for rule in self.rules:
                    thread = threading.Thread(target=rule.analyze, args=())
                    threads[thread.__class__] = thread
                    thread.setDaemon(True)
                    thread.start()
                for thread in threads:
                    threads[thread].join()
        except Exception as e:
            exit_end(self.paramters)
        self.end_analyze()

    def end_analyze(self):
        for rule in self.rules:
            rule.output()
        all_problems = self.result.merge_all_result()
        if len(all_problems) == 0:
            print("LocalLint analyze finished, no errors")
            return
        self.result.write_result(self.paramters.output_path)

        exit_end(self.paramters)