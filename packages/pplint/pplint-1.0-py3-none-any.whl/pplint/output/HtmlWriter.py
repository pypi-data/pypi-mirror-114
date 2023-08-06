import os
import time


class HtmlWriter:
    def __init__(self, path: str):
        self.file = None
        self.issues_map = {}
        self.path = path
        self.statistics = {"error": 0, "warning": 0, "info": 0}

    def write_report(self, all_report):
        self.get_issues_map(all_report)
        self.file = open(self.path, "w", encoding="utf-8")
        self.file.write(demo_html)
        self.write_body()
        self.file.write("""</html>\n""")
        self.file.close()

    def write_body(self):
        self.file.write("<body class=\"mdl-color--grey-100 mdl-color-text--grey-700 mdl-base\">\n")
        self.file.write("""<div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">\n""")
        self.write_navigation_header()
        self.write_drawer()
        self.write_main()
        self.file.write("""</div>\n""")
        self.file.write("</body>\n")

    def write_navigation_header(self):
        for severity in self.issues_map.keys():
            issues = self.issues_map[severity]
            for issues_id in issues:
                self.statistics[severity] += len(issues[issues_id])

        self.file.write("""<header class="mdl-layout__header">\n""")
        self.file.write("""<div class="mdl-layout__header-row">\n""")
        self.file.write("""<span class="mdl-layout-title">LocalLint Report:
             error: %s    warning: %s     info: %s</span>\n""" % (
            self.statistics["error"], self.statistics["warning"], self.statistics["info"]))
        self.file.write("""      <div class=\"mdl-layout-spacer\"></div>\n""")
        localtime = time.asctime(time.localtime(time.time()))
        self.file.write("""      <nav class=\"mdl-navigation mdl-layout--large-screen-only\">%s</nav>\n""" % (
            localtime))
        self.file.write("""      </div>\n""")
        self.file.write("""</header>\n""")

    def write_drawer(self):
        self.file.write("""<div class="mdl-layout__drawer">\n""")
        self.file.write("""<span class="mdl-layout-title">Issue Types</span>\n""")
        self.file.write("""<nav class="mdl-navigation">\n""")
        self.file.write("""<a class="mdl-navigation__link" href="#overview">""" +
                        """<i class="material-icons">dashboard</i>Overview</a>\n""")
        for severity in self.issues_map.keys():
            issues = self.issues_map[severity]
            for issue_id in issues.keys():
                self.file.write("""<a class="mdl-navigation__link" href="#%s">""" % issue_id +
                                """<i class="material-icons error-icon">%s</i>%s (%s)</a>\n""" % (
                                    severity, issue_id, len(issues[issue_id])))

        self.file.write("""</nav>\n""")
        self.file.write("""</div>\n""")

    def write_main(self):
        self.file.write("""<main class="mdl-layout__content">\n""")
        self.file.write("""<div class="mdl-layout__tab-panel is-active">\n""")
        self.write_overview()
        for severity in self.issues_map.keys():
            issues = self.issues_map[severity]
            keys = list(issues.keys())
            keys.sort()
            for issue_id in keys:
                self.write_issues_card(severity, issue_id, issues[issue_id])

    def write_overview(self):
        self.file.write("""<a name="overview"></a>\n""")
        self.file.write("""<section class="section--center mdl-grid mdl-grid--no-spacing 
                mdl-shadow--2dp" id="OverviewCard" style="display: block;">\n""")
        self.file.write("""<div class="mdl-card mdl-cell mdl-cell--12-col">\n""")
        self.file.write("""<div class="mdl-card__title">\n""")
        self.file.write("""<h2 class="mdl-card__title-text">Overview</h2>\n""")
        self.file.write("""</div>\n""")
        self.file.write("""<div class="mdl-card__supporting-text">\n""")
        self.file.write("""<table class="overview">\n""")
        for severity in self.issues_map.keys():
            issues = self.issues_map[severity]
            keys = list(issues.keys())
            keys.sort()
            for issue_id in keys:
                self.file.write("""<tr>\n""")
                self.file.write("""<td class="countColumn">%s</td>\n""" % len(issues[issue_id]))
                self.file.write("""<td class="issueColumn">\n""")
                self.file.write("""<i class="material-icons error-icon">%s</i>\n""" % severity)
                self.file.write("""<a href="#%s">%s</a>\n""" % (issue_id, issue_id))
                self.file.write(""": %s</td></tr>\n""" % issue_id)
        self.file.write("""</table></div></div></section>\n""")

    def write_issues_card(self, severity, issue_id, issues):
        self.file.write("""<a name="%s">\n""" % issue_id)
        self.file.write("""<section class="section--center mdl-grid mdl-grid--no-spacing 
                        mdl-shadow--2dp" id="%s" style="display: block;">\n""" % issue_id)
        self.file.write("""<div class="mdl-card mdl-cell mdl-cell--12-col">\n""")
        self.file.write("""<div class="mdl-card__title">\n""")
        self.file.write("""<h2 class="mdl-card__title-text">%s</h2>\n""" % issue_id)
        self.file.write("""</div>\n""")
        self.file.write("""<div class="mdl-card__supporting-text">\n""")
        self.file.write("""<div class="issue">\n""")
        self.file.write("""<div class="warningslist">\n""")
        issues_ext = []
        if len(issues) > 5:
            issues_ext = issues[5:]
            issues = issues[0:5]
        for issue in issues:
            self.write_issue(issue)
        if len(issues_ext) != 0:
            self.file.write("""<button class="mdl-button mdl-js-button mdl-button--primary" 
            id="%sDivLink" onclick="reveal('%sDiv');" />\n""" % (issue_id, issue_id))
            self.file.write("""+ %s More Occurrences...</button>""" % (len(issues_ext)))
            self.file.write("""<div id="%sDiv" style="display: none">\n""" % issue_id)
            for issue in issues_ext:
                self.write_issue(issue)
            self.file.write("""</div>\n""")
        self.file.write("""</div>\n""")
        self.file.write("""</div>\n""")
        self.file.write("""<div class="chips">\n""")
        self.file.write("""</div>\n""")
        self.file.write("""</div>\n""")
        self.file.write("""</div>\n""")
        self.file.write("""</section>\n""")

    def write_issue(self, issue):
        self.file.write("""<span class="location">\n""")
        self.file.write("""<a href="%s">%s</a>\n""" % (
            issue["report_location"]["file"], issue["report_location"]["file"]))
        self.file.write(""":%s</span><span class="message">\n""" % issue["report_location"]["start_line"])
        self.file.write("""<br/><br/>\n""")
        self.file.write("""%s</span><br/>\n""" % issue["explanation"])
        self.file.write("""<pre class="errorlines">\n""")
        self.write_error_code(issue["report_location"])
        self.file.write("""</pre>\n""")
        self.file.write("""<ul></ul>\n""")

    def write_error_code(self, location):
        if not os.path.exists(location["file"]):
            return
        code_file = open(location["file"], "r", encoding="utf-8")
        start_line = int(location["start_line"])
        end_line = int(location["end_line"])
        lines = end_line - start_line + 1

        if lines < 10:
            start = start_line - (10 - lines) / 2
        else:
            start = start_line
        if start < 1:
            start = 1
        i = 1
        start = int(start)
        for line in code_file.readlines():
            if start <= i <= start + 9:
                if start_line <= i <= end_line:
                    self.file.write("""<span class="lineno">%s</span><span class="caretline">%s</span>""" % (i, line))
                else:
                    self.file.write("""<span class="lineno">%s</span>%s""" % (i, line))
            i = i + 1

    def get_issues_map(self, all_report):
        for report in all_report:
            if report["severity"] in self.issues_map:
                if report["name"] in self.issues_map[report["severity"]]:
                    self.issues_map[report["severity"]][report["name"]].append(report)
                else:
                    self.issues_map[report["severity"]][report["name"]] = [report]
            else:
                self.issues_map[report["severity"]] = {report["name"]: [report]}


demo_html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Local Report</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
 <link rel="stylesheet" href="https://code.getmdl.io/1.2.1/material.blue-indigo.min.css" />
<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:300,400,500,700" type="text/css">
<script defer src="https://code.getmdl.io/1.2.0/material.min.js"></script>
    <style>
    section.section--center {
    max-width: 860px;
}
.mdl-card__supporting-text + .mdl-card__actions {
    border-top: 1px solid rgba(0, 0, 0, 0.12);
}
main > .mdl-layout__tab-panel {
  padding: 8px;
  padding-top: 48px;
}

.mdl-card__actions {
    margin: 0;
    padding: 4px 40px;
    color: inherit;
}
.mdl-card > * {
    height: auto;
}
.mdl-card__actions a {
    color: #00BCD4;
    margin: 0;
}
.error-icon {
    color: #bb7777;
    vertical-align: bottom;
}
.warning-icon {
    vertical-align: bottom;
}
.mdl-layout__content section:not(:last-of-type) {
  position: relative;
  margin-bottom: 48px;
}

.mdl-card .mdl-card__supporting-text {
  margin: 40px;
  -webkit-flex-grow: 1;
      -ms-flex-positive: 1;
          flex-grow: 1;
  padding: 0;
  color: inherit;
  width: calc(100% - 80px);
}
div.mdl-layout__drawer-button .material-icons {
    line-height: 48px;
}
.mdl-card .mdl-card__supporting-text {
    margin-top: 0px;
}
.chips {
    float: right;
    vertical-align: middle;
}
pre.errorlines {
    background-color: white;
    font-family: monospace;
    border: 1px solid #e0e0e0;
    line-height: 0.9rem;
    font-size: 0.9rem;    padding: 1px 0px 1px; 1px;
    overflow: scroll;
}
.prefix {
    color: #660e7a;
    font-weight: bold;
}
.attribute {
    color: #0000ff;
    font-weight: bold;
}
.value {
    color: #008000;
    font-weight: bold;
}
.tag {
    color: #000080;
    font-weight: bold;
}
.comment {
    color: #808080;
    font-style: italic;
}
.javadoc {
    color: #808080;
    font-style: italic;
}
.annotation {
    color: #808000;
}
.string {
    color: #008000;
    font-weight: bold;
}
.number {
    color: #0000ff;
}
.keyword {
    color: #000080;
    font-weight: bold;
}
.caretline {
    background-color: #fffae3;
}
.lineno {
    color: #999999;
    background-color: #f0f0f0;
}
.error {
    text-decoration: underline wavy #ff0000;
    text-decoration-color: #ff0000;
    -webkit-text-decoration-color: #ff0000;
    -moz-text-decoration-color: #ff0000;
}
.warning {
    text-decoration: none;
    background-color: #f6ebbc;
}
.overview {
    padding: 10pt;
    width: 100%;
    overflow: auto;
    border-collapse:collapse;
}
.overview tr {
    border-bottom: solid 1px #eeeeee;
}
.categoryColumn a {
     text-decoration: none;
     color: inherit;
}
.countColumn {
    text-align: right;
    padding-right: 20px;
    width: 50px;
}
.issueColumn {
   padding-left: 16px;
}
.categoryColumn {
   position: relative;
   left: -50px;
   padding-top: 20px;
   padding-bottom: 5px;
}
</style>
    <script language="javascript" type="text/javascript">
<!--
function reveal(id) {
if (document.getElementById) {
document.getElementById(id).style.display = 'block';
document.getElementById(id+'Link').style.display = 'none';
}
}
function hideid(id) {
if (document.getElementById) {
document.getElementById(id).style.display = 'none';
}
}
//-->
</script>
</head>"""
