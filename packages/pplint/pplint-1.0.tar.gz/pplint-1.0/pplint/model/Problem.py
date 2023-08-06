
class ProblemLevel:
    UNKNOWN = 'unkonwn'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'

    @staticmethod
    def get_level_map_bits(level):
        if level.lower() == "p0":
            return ProblemLevel.ERROR
        elif level.lower() == "p1":
            return ProblemLevel.WARNING
        elif level.lower() == "p2":
            return ProblemLevel.INFO


class Problem:
    name = ""
    line = ""
    location = None
    category = ""
    explanation = ""
    severity = ProblemLevel.UNKNOWN
    def __init__(self, name, severity, explanation, line, location):
        self.name = name
        self.severity = severity
        self.line = line
        self.location = location
        self.explanation = explanation

    def encode(self):
        return {"name": self.name,
                "severity": self.severity,
                "explanation": self.explanation,
                "line": self.line,
                "report_location": self.location.encode()}
