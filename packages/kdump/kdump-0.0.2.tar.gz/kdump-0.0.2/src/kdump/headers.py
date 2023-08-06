import pprint

from macho.macho import MachO
from objectivec.objcclass import Class
from .classlist import Classlist


class HeaderGenerator:
    def __init__(self, macho: MachO, classlist: Classlist):
        self.macho = macho
        self.headers = {}
        self.classlist = classlist

        for objc_class in classlist.list:
            self.headers[objc_class.name + '.h'] = Header(macho, classlist, objc_class)


        self.umbrella = UmbrellaHeader(self.headers)
        self.headers[self.macho.name + '.h'] = self.umbrella
        self.headers[self.macho.name + '-Structs.h'] = StructHeader(macho)


class UmbrellaHeader:
    def __init__(self, header_list: dict):
        self.text = "\n\n"
        for header in header_list.keys():
            self.text += "#include \"" + header + "\"\n"

    def __str__(self):
        return self.text

class StructHeader:
    def __init__(self, macho: MachO):
        text = ""

        for struct in macho.tp.structs.values():
            text += str(struct) + '\n\n'

        self.text = text



    def __str__(self):
        return self.text


class Header:
    def __init__(self, macho: MachO, classlist: Classlist, objcclass: Class):
        self.macho = macho
        self.objc_class = objcclass
        self.classlist = classlist

        self.properties = []
        self.methods = []
        self.ivars = []
        self.structs = []

        # just store these so we know not to display them
        self.getters = []
        self.setters = []

        self._process_properties()
        self._process_methods()
        self._process_ivars()

        self.self_importing_classnames = self._process_self_imports()
        self.self_importing_classnames.append(self.macho.name + '-Structs')
        self.text = self._generate_text()

    def __str__(self):
        return self.text

    def _generate_text(self):

        imports = ""
        for libname in self.objc_class.linkedlibs:
            # '/System/Library/Frameworks/UIKit.framework/UIKit']
            binname = libname.split('/')[-1]
            if binname != "":
                imports += '#include <' + binname + '/' + binname +'.h>\n'
        if len(self.self_importing_classnames) > 0:
            imports += "\n"
            for classname in self.self_importing_classnames:
                imports += '#include "' + classname + '.h"\n'

        ifndef = "#ifndef " + self.objc_class.name.upper() + "_H\n"
        ifndef += "#define " +  self.objc_class.name.upper() + "_H\n"

        head = "@interface " + self.objc_class.name + ' : '

        # Decode Superclass Name
        superclass = "NSObject"
        if self.objc_class.superclass != "":  # _OBJC_CLASS_$_UIApplication
            superclass = self.objc_class.superclass.split('_')[-1]

        head += superclass

        # Protocol Implementing Declaration
        if len(self.objc_class.protocols) > 0:
            head += " <"
            for prot in self.objc_class.protocols:
                head += str(prot) + ', '
            head = head[:-2]
            head += '>'

        # Ivar Declaration
        ivars = ""
        if len(self.ivars) > 0:
            ivars = " {\n"
            for ivar in self.ivars:
                ivars += '    ' + str(ivar) + ';\n'
            ivars += '}\n'


        props = ""
        for prop in self.properties:
            props += str(prop) + ';'
            if prop.ivarname != "":
                props += ' // ivar: ' + prop.ivarname + '\n'
            else:
                props += '\n'


        meths = ""
        for i in self.methods:
            meths += str(i) + ';\n'


        foot = "@end"

        endif = "#endif"
        return ifndef + '\n\n' + imports + '\n\n' + head + ivars + '\n\n' + props + '\n\n' + meths + '\n\n' + foot + '\n\n' + endif


    def _process_self_imports(self):
        self_import_classes = []
        for property in self.properties:
            for oclass in self.classlist.list:
                if oclass.name == property.type:
                    if oclass.name not in self_import_classes:
                        self_import_classes.append(oclass.name)
                        break
        for property in self.ivars:
            for oclass in self.classlist.list:
                if oclass.name == property.type:
                    if oclass.name not in self_import_classes:
                        self_import_classes.append(oclass.name)
                        break
        return self_import_classes

    def _process_properties(self):
        for property in self.objc_class.properties:
            if property.type.lower() == 'bool':
                gettername = 'is' + property.name[0].upper() + property.name[1:]
                self.getters.append(gettername)
            else:
                self.getters.append(property.name)
            if 'readonly' not in property.attributes:
                settername = 'set' + property.name[0].upper() + property.name[1:]
                self.setters.append(settername)
            self.properties.append(property)

    def _process_ivars(self):
        for ivar in self.objc_class.ivars:
            bad = False
            for prop in self.properties:
                if ivar.name == prop.ivarname:
                    bad = True
                    break
            if bad:
                continue
            self.ivars.append(ivar)

    def _process_methods(self):
        for method in self.objc_class.methods:
            bad = False
            for name in self.getters:
                if name in method.sel:
                    bad = True
                    break
            for name in self.setters:
                if name in method.sel:
                    bad = True
                    break
            if bad:
                continue
            self.methods.append(method)


