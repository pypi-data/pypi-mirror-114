class XmlWriter:

    def __init__(self, path: str):
        self.path = path

    def write_report(self, all_report):
        file = open(self.path, "w", encoding="utf-8")
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        file.write("<issues by=\"LocalLint\">\n")
        for report in all_report:
            self.write_issue(file, report, 1)
        file.write("</issues>\n")
        file.close()

    def write_issue(self, file, issue, indent):
        self.write_indent(file, indent)
        file.write("<issue\n")
        self.write_indent(file, indent + 1)
        file.write("name=\"%s\"\n" % issue["name"])
        self.write_indent(file, indent + 1)
        file.write("severity=\"%s\"\n" % issue["severity"])
        self.write_indent(file, indent + 1)
        file.write("explanation=\"%s\">\n" % issue["explanation"])
        if "report_location" in issue.keys():
            self.write_indent(file, indent + 1)
            file.write("<location\n")
            self.write_indent(file, indent + 2)
            file.write("file=\"%s\"\n" % issue["report_location"]["file"])
            self.write_indent(file, indent + 2)
            file.write("startLine=\"%s\"\n" % issue["report_location"]["start_line"])
            self.write_indent(file, indent + 2)
            file.write("startColumn=\"%s\"\n" % issue["report_location"]["start_column"])
            self.write_indent(file, indent + 2)
            file.write("endLine=\"%s\"\n" % issue["report_location"]["end_line"])
            self.write_indent(file, indent + 2)
            file.write("endColumn=\"%s\"/>\n" % issue["report_location"]["end_column"])
        self.write_indent(file, indent)
        file.write("</issue>\n\n")

    def write_indent(self, file, indent):
        for _ in range(0, indent):
            file.write("    ")
