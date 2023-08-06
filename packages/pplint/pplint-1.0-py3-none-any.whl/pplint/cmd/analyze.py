import getopt
import sys

from pplint.model.Parameters import Parameters
from pplint.manager.AnalyzeManager import AnalyzeManager

def analyze(argv):
    argv = sys.argv
    parameters = Parameters(argv)
    analyzeManager = AnalyzeManager(parameters)
    analyzeManager.start_analyze()