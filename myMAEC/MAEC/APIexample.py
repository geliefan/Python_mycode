# Import the required APIs
from maec.bundle.bundle import Bundle
from maec.bundle.malware_action import MalwareAction
from maec.utils import IDGenerator, set_id_method
from cybox.core import Object, AssociatedObjects, AssociatedObject, AssociationType
from cybox.objects.file_object import File

# Instantiate the MAEC/CybOX Entities
set_id_method(IDGenerator.METHOD_INT)
b = Bundle()
a = MalwareAction()
ao = AssociatedObject()

# Build the Associated Object for use in the Action
ao.properties = File()
ao.properties.file_name = "badware.exe"
ao.properties.size_in_bytes = "123456"
ao.association_type = AssociationType()
ao.association_type.value = 'output'
ao.association_type.xsi_type = 'maecVocabs:ActionObjectAssociationTypeVocab-1.0'

# Build the Action and add the Associated Object to it
a.name = 'create file'
a.name.xsi_type = 'maecVocabs:FileActionNameVocab-1.0'
a.associated_objects = AssociatedObjects()
a.associated_objects.append(ao)

# Add the Action to the Bundle
b.add_action(a)

# Output the Bundle to stdout
print b.to_xml(include_namespaces = False)
