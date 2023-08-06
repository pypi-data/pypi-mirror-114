from macho.util import *
from macho.structs import *

__all__ = ['Segment', 'Section']

class Segment:
    """


    segment_command_64:
    ["off", "cmd", "cmdsize", "segname", "vmaddr", "vmsize", "fileoff", "filesize",
        "maxprot", "initprot", "nsects", "flags"]
    """
    def __init__(self, fd, cmd):
        self.cmd = cmd
        self.vmaddr = cmd.vmaddr
        self.fileaddr = cmd.fileoff
        self.size = cmd.vmsize
        self.name = cmd.segname # segname field, struct offset 8, length max 16 bytes
        self.sections = self._process_sections(fd, cmd)

    def _process_sections(self, fd, cmd):
        sections = {}
        ea = cmd.off + sizeof(segment_command_64_t)

        for section in range(0, cmd.nsects):
            sect = load_struct(fd, ea, section_64_t)
            section = Section(fd, self, sect)
            sections[section.name] = section
            ea += sizeof(section_64_t)

        ea += sizeof(segment_command_64_t)
        return sections


class Section:
    """


    section_64
     ["off",
     "sectname",
     "segname",
     "addr", VM ADDRESS
     "size", SIZE ON BOTH
     "offset", FILE ADDRESS
     "align", "reloff", "nreloc", "flags", "void1", "void2", "void3"]
    """
    def __init__(self, fd, segment, cmd):
        self.cmd = cmd
        self.segment = segment
        self.name = getCStrAt(fd, cmd.off, 16)
        self.vmaddr = cmd.addr
        self.fileaddr = cmd.offset
        self.size = cmd.size
