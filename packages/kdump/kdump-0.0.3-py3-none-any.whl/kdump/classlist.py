from kdump.macho.segment import Section
from kdump.objectivec.objcclass import Class

class Classlist:
    def __init__(self, macho, classlimit=None):
        self.macho = macho
        self.list = self._generate_classlist(classlimit)

    def _generate_classlist(self, classlimit):
        sect: Section = self.macho.segments['__DATA_CONST'].sections['__objc_classlist']
        classes = []
        cnt = sect.size // 0x8
        for i in range(0, cnt):
            if classlimit == None:
                classes.append(Class(self.macho, sect.vmaddr + i * 0x8))
            else:
                oc = Class(self.macho, sect.vmaddr + i * 0x8)
                if classlimit == oc.name:
                    classes.append(oc)
        return classes
