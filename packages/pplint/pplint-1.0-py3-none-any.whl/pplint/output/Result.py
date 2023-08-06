import os
import subprocess
from pplint.model.Problem import ProblemLevel
from pplint.output.XmlWriter import XmlWriter
from pplint.output.HtmlWriter import HtmlWriter

class Result:
    issues = {}
    xml_writer = None
    html_writer = None

    def add_result(self, rule_name, problems):
        if rule_name not in self.issues:
            self.issues[rule_name] = {
                ProblemLevel.ERROR: [],
                ProblemLevel.WARNING: [],
                ProblemLevel.INFO: []
            }
        for problem in problems:
            problem["severity"] = problem["severity"].lower()
            self.issues[rule_name][problem["severity"]].append(problem)

    def merge_all_result(self):
        issues = []
        for rule_name in self.issues:
            for severity in self.issues[rule_name]:
                issues.extend(self.issues[rule_name][severity])
        return issues

    def write_result(self, path):
        xml_path = os.path.join(path, 'LocalLint-report.xml')
        html_path = os.path.join(path, 'LocalLint-report.html')
        if os.path.exists(xml_path):
            os.remove(xml_path)
        if os.path.exists(html_path):
            os.remove(html_path)
        self.xml_writer = XmlWriter(xml_path)
        self.xml_writer.write_report(self.merge_all_result())
        self.html_writer = HtmlWriter(html_path)
        self.html_writer.write_report(self.merge_all_result())
        subprocess.getstatusoutput('open %s' % html_path)
