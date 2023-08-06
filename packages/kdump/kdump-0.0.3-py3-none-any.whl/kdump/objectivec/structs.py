
from collections import namedtuple
from kdump.macho.util import *

"""
C Struct representation in Python
I have done what I can to make the syntax used similar to C syntax

The `struct` variable is a subclass of Tuple which contains a struct 'typedef' and a list of byte sizes for each field in the struct, in order.
"""
struct = namedtuple("struct", ["struct", "sizes"])

"""
OBJC STRUCTS
VALUES OF FIELDS SHOULD LINE UP WITH THOSE IN OBJC4 SOURCE
"""
objc2_class = namedtuple("objc2_class", ["off", "isa", "superclass", "cache", "vtable", "info"])
objc2_class_t = struct(objc2_class, [8, 8, 8, 8, 8])
objc2_class_ro = namedtuple("objc2_class_ro", ["off", "flags", "ivar_base_start", "ivar_base_size", "reserved", "ivar_lyt", "name", "base_meths", "base_prots", "ivars", "weak_ivar_lyt", "base_props"])
objc2_class_ro_t = struct(objc2_class_ro, [4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8])

objc2_meth = namedtuple("objc2_meth", ["off", "selector", "types", "imp"])
objc2_meth_t = struct(objc2_meth, [8, 8, 8])
objc2_meth_list_entry_t = struct(objc2_meth, [4,4,4])
objc2_meth_list = namedtuple("objc2_meth_list", ["off", "entrysize", "count"])
objc2_meth_list_t = struct(objc2_meth_list, [4, 4])

objc2_prop_list = namedtuple("objc2_prop_list", ["off", "entrysize", "count"])
objc2_prop_list_t = struct(objc2_prop_list, [4, 4])

objc2_prop = namedtuple("objc2_prop", ["off", "name", "attr"])
objc2_prop_t = struct(objc2_prop, [8, 8])

objc2_prot_list = namedtuple("objc2_prot_list", ["off", "cnt"])
objc2_prot_list_t = struct(objc2_prot_list, [8])

objc2_prot = namedtuple("objc2_prot", ["off", "isa", "name", "prots", "inst_meths", "class_meths", "opt_inst_meths", "opt_class_meths", "inst_props", "cb", "flags"])
objc2_prot_t = struct(objc2_prot, [8, 8, 8, 8, 8, 8, 8, 8, 4, 4])

objc2_ivar_list = namedtuple("objc2_ivar_list", ["off", "entrysize", "cnt"])
objc2_ivar_list_t = struct(objc2_ivar_list, [4, 4])

objc2_ivar = namedtuple("objc2_ivar", ["off", "offs", "name", "type", "align", "size"])
objc2_ivar_t = struct(objc2_ivar, [8, 8, 8, 4, 4])


def load_struct(fd: bytes, addr: int, aStruct: struct):
    sizeOf = sum(aStruct.sizes)
    fieldNames = list(aStruct.struct.__dict__['_fields']) #unimportant?
    fields = [addr]
    data = fd[addr:addr+sizeOf]
    ea = 0

    for field in aStruct.sizes:
        field_data = data[ea:ea+field]
        if field==16:
            try:
                fields.append(getStrAt(field_data, 0, 16))
            except:
                fields.append(getAt(field_data, 0, field))
        else:
            fields.append(getAt(field_data, 0, field))
        ea+=field

    if len(fields) != len(fieldNames):
        raise ValueError(f'Field-Fieldname count mismatch in load_struct for {struct.struct.__doc__}.\nCheck Fields and Size Array.')

    return aStruct.struct._make(fields)

def sizeof(t: struct):
    assert isinstance(t, struct)
    return sum(t.sizes)