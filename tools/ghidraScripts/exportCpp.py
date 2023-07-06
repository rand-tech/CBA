#export to cpp
#@author @rand6d74

from java.io import File
from ghidra.app.util.exporter import CppExporter
from ghidra.app.util import Option

def main(outputFile):
    cppExporter = CppExporter()
    options = [Option(CppExporter.CREATE_HEADER_FILE, False)]
    cppExporter.setOptions(options)
    cppExporter.setExporterServiceProvider(state.getTool())
    cppExporter.export(File(outputFile), currentProgram, None, monitor)

if __name__ == '__main__':
    outputFile = getScriptArgs()[0]
    main(outputFile)
