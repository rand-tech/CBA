#gzf export script
#@author @rand6d74

from ghidra.program.model.listing import *
from ghidra.program.model.symbol import *
from ghidra.app.cmd.label import *
from ghidra.program.model.symbol.SourceType import *
from java.io import File


def export_to_gzf(gzf_filename):

    # commit transaction
    # https://ghidra.re/ghidra_docs/api/ghidra/program/flatapi/FlatProgramAPI.html#end(boolean)
    end(True)

    program = getCurrentProgram()
    df = program.getDomainFile()
    outfile = File(gzf_filename)
    # https://github.com/NationalSecurityAgency/ghidra/issues/2127
    df.packFile(outfile, monitor)
    print('[*] saved {}'.format(gzf_filename))


if __name__ == '__main__':
    args = getScriptArgs()
    gzf_filename = str(args[0])
    export_to_gzf(gzf_filename)
