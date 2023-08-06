from .structs import *
from .method import Method
from .property import Property
from .protocol import Protocol
from .ivar import Ivar

from macho.macho import MachO
from macho.vm import VirtualMemoryMap
from macho.util import *


class Class:
    """
    Objective C Class
    This can be a superclass, metaclass, etc
    can represent literally anything that's a "class" struct


    objc2_class = ["off", "isa", "superclass", "cache", "vtable",
    "info" :  VM pointer to objc2_class_ro
    ]

    objc2_class_ro = ["off", "flags", "ivar_base_start", "ivar_base_size", "reserved", "ivar_lyt", "name", "base_meths", "base_prots", "ivars", "weak_ivar_lyt", "base_props"]
    """

    def __init__(self, macho: MachO, ptr: int):
        self.macho = macho
        self.meta = False
        self.superclass = ""
        self.linkedlibs = []
        # Classes imported in this class from the same mach-o

        self.objc2_class: objc2_class = self._load_objc2_class(macho, ptr)
        objc2_class_ro_location = macho.vm.get_file_address(self.objc2_class.info)
        self.objc2_class_ro = load_struct(macho.fd, objc2_class_ro_location, objc2_class_ro_t)
        #print(hex(objc2_class_location))
        self._process_structs()


        self.methods = self._process_methods()
        self.properties = self._process_props()
        self.protocols = self._process_prots()
        #print(self.superclass)
        #print(self.linkedlibs)
        self.ivars = self._process_ivars()
        self._load_linked_libraries()


    def __str__(self):
        ret = ""
        ret += self.name
        return ret

    def _load_linked_libraries(self):
        for classname, libname in self.macho.binding_classnames.items():
            for property in self.properties:
                if property.type == classname:
                    if libname not in self.linkedlibs:
                        self.linkedlibs.append(libname)
            for ivar in self.ivars:
                if ivar.type == classname:
                    if libname not in self.linkedlibs:
                        self.linkedlibs.append(libname)

    def _load_objc2_class(self, macho, ptr):
        objc2_class_location_location = macho.vm.get_file_address(ptr)
        objc2_class_location = macho.vm.get_file_address(getAt(macho.fd, objc2_class_location_location, 8))
        objc2_class_item: objc2_class = load_struct(macho.fd, objc2_class_location, objc2_class_t)
        bad_addr = False
        try:
            objc2_superclass: objc2_class = load_struct(macho.fd, macho.vm.get_file_address(objc2_class_item.superclass), objc2_class_t)

        except:
            bad_addr = True

        if bad_addr:
            # Linked Superclass
            struct_size = sizeof(objc2_class_t)
            struct_location = objc2_class_item.off
            for action in macho.binding_actions:
                try:
                    action_file_location = macho.vm.get_file_address(action.vmaddr)
                except ValueError:
                    continue
                if action_file_location == struct_location + 0x8:
                    self.superclass = action.item
                    self.linkedlibs.append(action.libname)
                    break
        else:
            try:
                self.superclass = Class(self.macho, objc2_class_item.superclass).name
            except:
                pass
        return objc2_class_item

    def _process_structs(self):
        name_location = self.macho.vm.get_file_address(self.objc2_class_ro.name)
        self.name = getCStrAt(self.macho.fd, name_location)

    def _process_methods(self):
        methods = []

        if self.objc2_class_ro.base_meths == 0:
            return methods # Useless Subclass

        ea = self.macho.vm.get_file_address(self.objc2_class_ro.base_meths)
        vm_ea = self.objc2_class_ro.base_meths
        methlist_head = load_struct(self.macho.fd, ea, objc2_meth_list_t)

        # https://github.com/arandomdev/DyldExtractor/blob/master/DyldExtractor/objc/objc_structs.py#L79
        RELATIVE_METHODS_SELECTORS_ARE_DIRECT_FLAG = 0x40000000
        RELATIVE_METHOD_FLAG = 0x80000000
        METHOD_LIST_FLAGS_MASK = 0xFFFF0000

        uses_relative_methods = methlist_head.entrysize & METHOD_LIST_FLAGS_MASK != 0

        ea += 8
        vm_ea += 8
        for i in range(1, methlist_head.count+1):
            if uses_relative_methods:
                meth = load_struct(self.macho.fd, ea, objc2_meth_list_entry_t)
            else:
                meth = load_struct(self.macho.fd, ea, objc2_meth_t)
            try:
                methods.append(Method(self.macho, self, meth, vm_ea))
            except Exception as ex:
                raise ex
            if uses_relative_methods:
                ea += sizeof(objc2_meth_list_entry_t)
                vm_ea += sizeof(objc2_meth_list_entry_t)
            else:
                ea += sizeof(objc2_meth_t)
                vm_ea += sizeof(objc2_meth_t)

        return methods

    def _process_props(self):
        properties = []

        if self.objc2_class_ro.base_props == 0:
            return properties

        ea = self.macho.vm.get_file_address(self.objc2_class_ro.base_props)
        vm_ea = self.objc2_class_ro.base_props
        proplist_head = load_struct(self.macho.fd, ea, objc2_prop_list_t)
        ea += 8
        vm_ea += 8

        for i in range(1, proplist_head.count+1):
            prop = load_struct(self.macho.fd, ea, objc2_prop_t)
            try:
                properties.append(Property(self.macho, self, prop, vm_ea))
            except ValueError as ex:
                # continue
                raise ex
            ea += sizeof(objc2_prop_t)
            vm_ea += sizeof(objc2_prop_t)

        return properties

    def _process_prots(self):
        prots = []
        if self.objc2_class_ro.base_prots == 0:
            return prots
        protlist_loc = self.macho.vm.get_file_address(self.objc2_class_ro.base_prots)
        protlist: objc2_prot_list = load_struct(self.macho.fd, protlist_loc, objc2_prot_list_t)
        ea = protlist.off
        for i in range(1, protlist.cnt+1):
            prot_loc_loc = ea + i*8
            prot_loc = self.macho.vm.get_file_address(getAt(self.macho.fd, prot_loc_loc, 8))
            prots.append(Protocol(self.macho, self, load_struct(self.macho.fd, prot_loc, objc2_prot_t), prot_loc))
        return prots

    def _process_ivars(self):
        ivars = []
        if self.objc2_class_ro.ivars == 0:
            return ivars
        ivarlist_loc = self.macho.vm.get_file_address(self.objc2_class_ro.ivars)
        ivarlist: objc2_ivar_list = load_struct(self.macho.fd, ivarlist_loc, objc2_ivar_list_t)
        ea = ivarlist.off + 8
        for i in range(1, ivarlist.cnt+1):
            ivar_loc = ea + sizeof(objc2_ivar_t)*(i-1)
            ivars.append(Ivar(self.macho, self, load_struct(self.macho.fd, ivar_loc, objc2_ivar_t), ivar_loc))
        return ivars