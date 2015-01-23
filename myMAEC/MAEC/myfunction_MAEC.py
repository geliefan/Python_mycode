'''
Created on 2015/01/17

@author: Makoto
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    # Actionで使うための関連オブジェクトのディクショナリーを作成
    def associated(name,path,byte,value="output"):
        associated_object = AssociatedObject()
        associated_object.properties = File() #ここがObjectによってことなるんだよね～
        associated_object.properties.file_name = name
        associated_object.properties.file_path = path
        associated_object.properties.size_in_bytes = byte
        associated_object.association_type = VocabString() #これはなんだ？
        associated_object.association_type.value = value
        associated_object.association_type.xsi_type = 'maecVocabs:ActionObjectAssociationTypeVocab-1.0'
        return associated_object
        