#  file_writes
def file_writes(fname):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Write to File"
    a.type_ = "Write"

    ao.properties = WinFile()
    ao.properties.path = fname

    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    print a     # debug print
    return a

if __name__ == '__main__':
    file_writes = [
                ]
    for n in file_writes:
        filename =  n["filename"]
        print type(filename)
        b = []
        a = file_writes("test")
