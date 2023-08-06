
from .structs import *
from .type import *

from macho.macho import *
from macho.util import *

# 00000000
# 00000000 __objc2_ivar    struc ; (sizeof=0x20, align=0x8, copyof_43)

# 00000000 offs            DCQ ?  ; VM Address, stores the actual static location of the variable
# 00000008 name            DCQ ?  ; VM Address, pointer to the name string
# 00000010 type            DCQ ?  ; VM Address, String offset, `@"TypeName"0x00` style type string
# 00000018 align           DCD ?  ; Align
# 0000001C size            DCD ?  ; Size in bytes of the ivar at `offs`
# 00000020 __objc2_ivar    ends
# 00000020


class Ivar:
    def __init__(self, macho: MachO, objc_class, ivar: objc2_ivar, vmaddr: int):
        name_loc = macho.vm.get_file_address(ivar.name, "__objc_methname")
        self.name = getCStrAt(macho.fd, name_loc)
        type_loc = macho.vm.get_file_address(ivar.type, "__objc_methtype")
        type_string = getCStrAt(macho.fd, type_loc)
        self.is_id = type_string[0] == "@"
        self.type = self._renderable_type(macho.tp.process(type_string)[0])

    def __str__(self):
        ret = ""
        ret += self.type + ' '
        if self.is_id:
            ret += '*'
        ret += self.name
        return ret

    @staticmethod
    def _renderable_type(type: Type):
        if type.type == EncodedType.NORMAL:
            return str(type)
        elif type.type == EncodedType.STRUCT:
            ptraddon = ""
            for i in range(0, type.pointer_count):
                ptraddon += '*'
            return ptraddon + type.value.name
        return(str(type))