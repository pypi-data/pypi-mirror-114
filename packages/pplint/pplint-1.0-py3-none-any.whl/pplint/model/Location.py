

class Location:
    file = ""
    start_line = ""
    end_line = ""

    def __init__(self, file, start_line, end_line):
        self.file = file
        self.start_line = start_line
        self.end_line = end_line

    def encode(self):
        return {"file": self.file,
                "start_line": self.start_line,
                "end_line": self.end_line,
                "start_column": 0,
                "end_column": 0
        }

