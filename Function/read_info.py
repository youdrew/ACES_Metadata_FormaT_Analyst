try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET



def Printinfo(amf_filepath):
    '''解析并打印amf文件中的信息'''
    # 解析amf文件,获取根节点root
    tree = ET.parse(amf_filepath)
    root = tree.getroot()
    amfinfo_rst = get_AMFInfo(root)
    clipid_rst = get_ClipID(root)
    return amfinfo_rst,clipid_rst


def get_AMFInfo(root):
    '''解析AMFinfo部分的四个信息
       description
       name
       emailAdress
       amfUUID'''

    rst = []
    amfInfo_description = 'None'
    amfInfo_name = 'None'
    amfInfo_emailAdress = 'None'
    amfInfo_amfUUID = 'None'
    # 找到root节点下的所有amfInfo节点
    for amfInfo in root.findall('{urn:ampas:aces:amf:v1.0}amfInfo'):

        # 查找amfInfo节点下的 description 节点
        description = amfInfo.find('{urn:ampas:aces:amf:v1.0}description')
        if description is not None:
            amfInfo_description = description.text

        # 查找amfInfo节点下的 name 节点
        name = amfInfo.find('{urn:ampas:aces:amf:v1.0}name')
        if name is not None:
            amfInfo_name = name.text

        # 查找amfInfo节点下的 emailAdress 节点
        emailAdress = amfInfo.find('{urn:ampas:aces:amf:v1.0}emailAdress')
        if emailAdress is not None:
            amfInfo_emailAdress = emailAdress.text

        # 查找amfInfo节点下的 amfUUID 节点
        amfUUID = amfInfo.find('{urn:ampas:aces:amf:v1.0}amfUUID')
        if amfUUID is not None:
            amfInfo_amfUUID = amfUUID.text

    rst.append(amfInfo_description)
    rst.append(amfInfo_name)
    rst.append(amfInfo_emailAdress)
    rst.append(amfInfo_amfUUID)
    return rst

    # # 设置AMFINFO下的几个文本框信息
    # self.ANALYSISPanel_Info_AMFInfo_TextEdit.setPlainText(amfInfo_description)
    # self.ANALYSISPanel_Info_Name_LineEdit.setText(amfInfo_name)
    # self.ANALYSISPanel_Info_EmailAddress_LineEdit.setText(amfInfo_emailAdress)
    # self.ANALYSISPanel_Info_AMFUUID_LineEdit.setText(amfInfo_amfUUID)

def get_ClipID(root):
    '''解析ClipID部分的五个信息
               description
               name
               ClipIDUUID
               ClipIDPath
               ClipIDSequence'''

    rst = []
    ClipID_description = 'None'
    ClipID_name = 'None'
    ClipID_UUID = 'None'
    ClipID_path = 'None'
    ClipID_sequence = 'None'

    # 找到 root 节点下的所有 clipId 节点
    clipId = root.find('{urn:ampas:aces:amf:v1.0}clipId')
    if clipId is not None:
        # 查找 clipId 节点下的 description 节点
        description = clipId.find('{urn:ampas:aces:amf:v1.0}description')
        if description is not None:
            ClipID_description = description.text

        # 查找 clipId 节点下的 clipName 节点
        clipName = clipId.find('{urn:ampas:aces:amf:v1.0}clipName')
        if clipName is not None:
            ClipID_name = clipName.text

        # 查找 clipId 节点下的 UUID 节点
        UUID = clipId.find('{urn:ampas:aces:amf:v1.0}UUID')
        if UUID is not None:
            ClipID_UUID = UUID.text

        # 查找 clipId 节点下的 file 节点
        file = clipId.find('{urn:ampas:aces:amf:v1.0}file')
        if file is not None:
            ClipID_path = file.text

        # 查找 clipId 节点下的 sequence 节点
        sequence = clipId.find('{urn:ampas:aces:amf:v1.0}sequence')
        if sequence is not None:
            ClipID_sequence = sequence.text

    rst.append(ClipID_description)
    rst.append(ClipID_name)
    rst.append(ClipID_UUID)
    rst.append(ClipID_path)
    rst.append(ClipID_sequence)
    return rst

    #
    #
    # # 设置ClipID下的几个文本框信息
    # self.ANALYSISPanel_Info_CilpID_TextEdit.setPlainText(ClipID_description)
    # self.ANALYSISPanel_Info_CilpName_LineEdit.setText(ClipID_name)
    # self.ANALYSISPanel_Info_CilpUUID_LineEdit.setText(ClipID_UUID)
    # self.ANALYSISPanel_Info_FilePath_LineEdit.setText(ClipID_path)
    # self.ANALYSISPanel_Info_Sequence_LineEdit.setText(ClipID_sequence)
