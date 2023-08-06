from kdump.objectivec.type import *
from .structs import *
from .segment import *
from .binding import *
from .vm import *

# macho_file = namedtuple("macho_file", ["header", "info", "segments", "installname", "linked", "vm"])
# macho_header = namedtuple("macho_header", ["header", "loadcmds"])

# dyld_header = namedtuple("dyld_header", ["off", "header", "cpu", "cput", "filetype", "loadcnt", "loadsze", "flags", "void"])
# dyld_header_t = struct(dyld_header, [4, 4, 4, 4, 4, 4, 4, 4])


class Library:
    """
    Represents any library including self and off-image ones


    """
    def __init__(self, fd, cmd):
        self.install_name = self._get_name(fd, cmd)
        self.local = cmd.cmd == 0xD

    @staticmethod
    def _get_name(fd, cmd):
        ea = cmd.off + sizeof(dylib_command_t)
        return getCStrAt(fd, ea)


class MachOHeader:
    """
    This class represents the Mach-O Header
    It contains the basic header info along with all load commands within it.

    It doesn't handle complex abstraction logic, it simply loads in the load commands as their raw structs
    """
    def __init__(self, fd: bytes):
        self.dyld_header: dyld_header = load_struct(fd, 0, dyld_header_t)
        self.load_commands = []
        self._process_load_commands(fd)

    def _process_load_commands(self, fd: bytes):
        """
        This function takes the raw file and parses through its load commands

        :param fd: file
        :return:
        """

        # Start address of the load commands.
        ea = 0x20

        # Loop through the dyld_header by load command count
        # possibly this could be modified to check for other load commands
        #       as a rare obfuscation technique involves fucking with these to screw with RE tools.

        for i in range(1, self.dyld_header.loadcnt):
            cmd = getAt(fd, ea, 4)
            try:
                loadcmd = load_struct(fd, ea, LOAD_COMMAND_TYPEMAP[cmd])
            except KeyError as ex:
                continue

            self.load_commands.append(loadcmd)
            ea += loadcmd.cmdsize


class MachO:
    """
    This class represents the Mach-O Binary as a whole.

    It's the root object in the massive tree of information we're going to build up about the binary

    This is an abstracted version, other classes will handle the raw struct interaction;
        here, we facilitate that interaction within those classes and generate our abstract representation

    Calling __init__ on this class will kickstart the full process.
    """
    def __init__(self, fd):
        self.fd = fd
        self.macho_header = MachOHeader(fd)
        self.linked = []
        self.segments = {}
        self.vm = VirtualMemoryMap(fd)
        self.tp = TypeProcessor()
        self.info = None
        self.dylib = None
        self._parse_load_commands(fd)
        self.binding_classnames = {}
        self.binding_actions = self._load_binding()
        if self.dylib is not None:
            self.name = self.dylib.install_name.split('/')[-1]
        else:
            self.name = ""

    def get_bytes(self, offset: int, length: int, vm=False):
        if vm:
            addr = self.vm.get_file_address(offset)
            return int.from_bytes(self.fd[addr:addr + length], "little")
        else:
            return int.from_bytes(self.fd[offset:offset + length], "little")

    def _load_binding(self):
        binding = BindingProcessor(self)

        for action in binding.actions:
            if '_OBJC_CLASS' in action.item:
                classname = action.item.split('_')[-1]
                self.binding_classnames[classname] = action.libname
        return binding.actions

    def _parse_load_commands(self, fd):
        for cmd in self.macho_header.load_commands:
            # my structLoad function *ALWAYS* saves the offset on-disk to the .off field, regardless of the struct
            #   loaded.
            ea = cmd.off

            if isinstance(cmd, segment_command_64):
                segment = Segment(fd, cmd)
                self.vm.add_segment(segment)
                self.segments[segment.name] = segment

            if isinstance(cmd, dyld_info_command):
                self.info = cmd

            if isinstance(cmd, dylib_command):
                ea += sizeof(dylib_command_t)
                if cmd.cmd == 0xD:  # local
                    self.dylib = Library(fd, cmd)
                else:
                    self.linked.append(Library(fd, cmd))