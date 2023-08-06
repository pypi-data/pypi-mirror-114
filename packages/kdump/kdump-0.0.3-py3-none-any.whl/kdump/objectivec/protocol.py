
from .structs import *
from kdump.macho.macho import MachO
from kdump.macho.util import getCStrAt

class Protocol:
    def __init__(self, macho: MachO, objc_class, protocol: objc2_prot, vmaddr: int):
        name_location = macho.vm.get_file_address(protocol.name)
        self.name = getCStrAt(macho.fd, name_location)

    def __str__(self):
        return self.name