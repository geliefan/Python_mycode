# Example 1 - Simple Package Generation Example
# Generates and exports MAEC Package with:
# - A single Malware Subject
# - A single Bundle embedded in the Malware Subject
# - A single Action embedded in the Bundle
# - A single Capability embedded in the Bundle

#セミナーの案内.docを対象とする

from cybox.core import AssociatedObjects, AssociatedObject, Object, AssociationType
from cybox.common import Hash, HashList
from cybox.objects.file_object import File
from maec.bundle.bundle import Bundle
from maec.bundle.malware_action import MalwareAction
from maec.bundle.capability import Capability
from maec.package.analysis import Analysis
from maec.package.malware_subject import MalwareSubject
from maec.package.package import Package
from cybox.utils import Namespace
import maec.utils

#NameSpace = malanalyze
NS = Namespace("http://malanalyze.com/", "malanalyze")
maec.utils.set_id_namespace(NS)
bundle = Bundle(defined_subject = False)
package = Package()
subject = MalwareSubject()
analysis = Analysis()
# Create the Object for use in the Malware Instance
subject_object = Object()
subject_object.properties = File()
subject_object.properties.name = 'セミナーのご案内.doc'
subject_object.properties.size_in_byte = ''
subject_object.properties.hashes = HashList()
subject_object.properties.hashes.append(Hash(''))
