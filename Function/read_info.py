try:
  import xml.etree.cElementTree as ET # 导入ElementTree模块
except ImportError:
  import xml.etree.ElementTree as ET


def Printinfo(amf_filepath):
    '''解析并打印amf文件中的信息'''
    # 解析amf文件,获取根节点root
    tree = ET.parse(amf_filepath)    #解析xml文件，得到树形结构 tree里包含了AMF内有所的文本信息
    root = tree.getroot()            #获取根节点 root是自定义变量 里面存储着aces:acesMetadataFile根节点下所有的内容


    '''解析根文件acesMetadataFile与root下的属性，新建2个局部变量，并把结果存储只啊acesMetadataFile_rst下
            xmlversion  (储存xml文件版本 属性是root下的version)
        schemaLocation （储存schema文件位置 属性是xsi:schemaLocation）
    '''
    global aces_amfVersionNumber
    global cdl_VersionNumber

    acesMetadataFile_rst = {}
    acesMetadataFile_rst['xmlversion'] = root.get('version')
    acesMetadataFile_rst['schemaLocation'] = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')


    #以下注释部分还在思考怎么写，想把xmlns:aces="urn:ampas:aces:amf:v1.0" xmlns:cdl="urn:ASC:CDL:v1.01" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"root中这段内容读取出来
    #a12345=root.keys()
    #print(a12345)
    #acesMetadataFile_rst['cdlversion'] = root.get('xmlns:cdl')

    aces_amfVersionNumber = '{'+acesMetadataFile_rst['schemaLocation'][:23]+'}'  #需要{urn:ampas:aces:amf:v1.0}这么一段内容加在搜索词前面，才能找到对应的元素
    cdl_VersionNumber

    amfinfo_rst = get_AMFInfo(root)
    clipid_rst = get_ClipID(root)
    pipeline_rst = get_pipeline(root)

    return acesMetadataFile_rst,amfinfo_rst,clipid_rst,pipeline_rst

# 任何一个转换都是依靠description、hash、uuid、file、transformId来确定具体的CTL文件的
def TransformFunction(WhichTransform, WhichChannel):
    TransformFunction_description = 'None'
    TransformFunction_hash = 'None'
    TransformFunction_uuid = 'None'
    TransformFunction_transformId = 'None'
    for WhichTransform in WhichChannel.iter(aces_amfVersionNumber + WhichTransform):
        if WhichTransform is not None:
            # 查找description
            TransformFunction_description = WhichTransform.find(aces_amfVersionNumber + 'description')
            if TransformFunction_description is not None:
                TransformFunction_description = TransformFunction_description.text
            # 查找hash
            TransformFunction_hash = WhichTransform.find(aces_amfVersionNumber + 'hash')
            if TransformFunction_hash is not None:
                TransformFunction_hash = TransformFunction_hash.text
            # 查找uuid
            TransformFunction_uuid = WhichTransform.find(aces_amfVersionNumber + 'uuid')
            if TransformFunction_uuid is not None:
                TransformFunction_uuid = TransformFunction_uuid.text
            # 查找file
            TransformFunction_file = WhichTransform.find(aces_amfVersionNumber + 'file')
            if TransformFunction_file is not None:
                TransformFunction_file = TransformFunction_file.text
            # 查找transfotransformId
            TransformFunction_transformId = WhichTransform.find(aces_amfVersionNumber + 'transformId')
            if TransformFunction_transformId is not None:
                TransformFunction_transformId = TransformFunction_transformId.text
    return TransformFunction_description, TransformFunction_hash, TransformFunction_uuid, TransformFunction_file ,TransformFunction_transformId


def get_AMFInfo(root):
    '''解析AMFinfo部分的信息,新建6个局部变量，并把最终结果存储在字典AMFInfo_rst
       description

       author_name
       author_emailAdress

       uuid

       dateTime_creationDateTime
       dateTime_modificationDateTime
       '''

    AMFInfo_rst = {}

    amfInfo_description = 'None'
    amfInfo_author_name = 'None'
    amfInfo_author_emailAdress = 'None'
    amfInfo_uuid = 'None'
    amfInfo_dateTime_creationDateTime = 'None'
    amfInfo_dateTime_modificationDateTime = 'None'

    # 找到root节点下的所有amfInfo节点
    for amfInfo in root.findall(aces_amfVersionNumber+'amfInfo'):

        # 查找amfInfo节点下的 description 节点
        description = amfInfo.find(aces_amfVersionNumber+'description')
        if description is not None:
            amfInfo_description = description.text

        # 查找amfInfo节点下的 author 节点 里面包含了name和emailAddress信息
        for author in amfInfo.iter(aces_amfVersionNumber + 'author'):
            amfInfo_author_name = author.find(aces_amfVersionNumber + 'name')
            if amfInfo_author_name is not None:
                amfInfo_author_name = amfInfo_author_name.text
            amfInfo_author_emailAdress = author.find(aces_amfVersionNumber + 'emailAddress')
            if amfInfo_author_emailAdress is not None:
                amfInfo_author_emailAdress = amfInfo_author_emailAdress.text

        # 查找amfInfo节点下的 amfUUID 节点
        amfInfo_uuid = amfInfo.find(aces_amfVersionNumber+'uuid')
        if amfInfo_uuid is not None:
            amfInfo_uuid = amfInfo_uuid.text
            amfInfo_uuid=amfInfo_uuid[9:]  #切片切除uuid前的描述"urn:uuid:"

        # 查找amfInfo节点下的 dateTime 节点 里面包含了creationDateTime和modificationDateTime信息
        for dateTime in amfInfo.iter(aces_amfVersionNumber + 'dateTime'):
            amfInfo_dateTime_creationDateTime = dateTime.find(aces_amfVersionNumber + 'creationDateTime')
            if amfInfo_dateTime_creationDateTime is not None:
                amfInfo_dateTime_creationDateTime = amfInfo_dateTime_creationDateTime.text
            amfInfo_dateTime_modificationDateTime = dateTime.find(aces_amfVersionNumber + 'modificationDateTime')
            if amfInfo_dateTime_modificationDateTime is not None:
                amfInfo_dateTime_modificationDateTime = amfInfo_dateTime_modificationDateTime.text

    AMFInfo_rst['description']=amfInfo_description
    AMFInfo_rst['author_name']=amfInfo_author_name
    AMFInfo_rst['author_emailAdress']=amfInfo_author_emailAdress
    AMFInfo_rst['uuid']=amfInfo_uuid
    AMFInfo_rst['dateTime_creationDateTime']=amfInfo_dateTime_creationDateTime
    AMFInfo_rst['dateTime_modificationDateTime']=amfInfo_dateTime_modificationDateTime
    return AMFInfo_rst


def get_ClipID(root):
    '''解析CilpID部分的信息,新建8个局部变量，并把最终结果存储在字典CilpID_rst
               description

               name

               ClipIDSequence
               ClipID_sequence_idx
               ClipID_sequence_min
               ClipID_sequence_max

               ClipIDPath
               ClipIDUUID

'''

    CilpID_rst = {}

    ClipID_description = 'None'
    ClipID_cilpname = 'None'
    ClipID_sequence = 'None'
    ClipID_sequence_idx = 'None'
    ClipID_sequence_min = 'None'
    ClipID_sequence_max = 'None'
    ClipID_path = 'None'
    ClipID_uuid = 'None'

    # 找到 root 节点下的所有 clipId 节点
    clipId = root.find(aces_amfVersionNumber+'clipId')
    if clipId is not None:
        # 查找 clipId 节点下的 description 节点
        description = clipId.find(aces_amfVersionNumber+'description')
        if description is not None:
            ClipID_description = description.text

        # 查找 clipId 节点下的 clipName 节点
        clipName = clipId.find(aces_amfVersionNumber+'clipName')
        if clipName is not None:
            ClipID_cilpname = clipName.text

        # 查找 clipId 节点下的 sequence 节点
        sequence = clipId.find(aces_amfVersionNumber+'sequence')
        if sequence is not None:
            ClipID_sequence = sequence.text
            ClipID_sequence_idx = sequence.get('idx')
            ClipID_sequence_min = sequence.get('min')
            ClipID_sequence_max = sequence.get('max')

        # 查找 clipId 节点下的 file 节点
        file = clipId.find(aces_amfVersionNumber + 'file')
        if file is not None:
            ClipID_path = file.text

        # 查找 clipId 节点下的 uuid 节点
        uuid = clipId.find(aces_amfVersionNumber + 'uuid')
        if uuid is not None:
            ClipID_uuid = uuid.text
            ClipID_uuid = ClipID_uuid[9:]  # 切片切除uuid前的描述"urn:uuid:"

    CilpID_rst['description']=ClipID_description
    CilpID_rst['cilpname']=ClipID_cilpname
    CilpID_rst['sequence']=ClipID_sequence
    CilpID_rst['sequence_idx']=ClipID_sequence_idx
    CilpID_rst['sequence_min']=ClipID_sequence_min
    CilpID_rst['sequence_max']=ClipID_sequence_max
    CilpID_rst['file']=ClipID_path
    CilpID_rst['uuid']=ClipID_uuid
    return CilpID_rst


def get_pipeline(root):
    '''
    解析单个pipeline部分的信息,新建 个局部变量，并把最终结果存储在字典pipeline1_rst

    pipelineInfo_description
    pipelineInfo_author_name
    pipelineInfo_author_emailAdress
    pipelineInfo_dateTime_creationDateTime
    pipelineInfo_dateTime_modificationDateTime
    pipelineInfo_uuid
    pipelineInfo_systemVersion_majorVersion
    pipelineInfo_systemVersion_minorVersion
    pipelineInfo_systemVersion_patchVersion

    //inputTransform
    inputTransform_applied
    inputTransform_description
    inputTransform_hash
    inputTransform_uuid
    inputTransform_file
    inputTransform_transformId

    //inverseOutputTransform
    inverseOutputTransform_applied
    inverseOutputTransform_description
    inverseOutputTransform_hash
    inverseOutputTransform_uuid
    inverseOutputTransform_file
    inverseOutputTransform_transformId

    //inverseOutputDeviceTransform
    inverseOutputDeviceTransform_applied
    inverseOutputDeviceTransform_description
    inverseOutputDeviceTransform_hash
    inverseOutputDeviceTransform_uuid
    inverseOutputDeviceTransform_file
    inverseOutputDeviceTransform_transformId

    //inverseReferenceRenderingTransform
    inverseReferenceRenderingTransform_applied
    inverseReferenceRenderingTransform_description
    inverseReferenceRenderingTransform_hash
    inverseReferenceRenderingTransform_uuid
    inverseReferenceRenderingTransform_file
    inverseReferenceRenderingTransform_transformId
    '''

    pipeline1_rst= {}

    pipeline1_rst_description = 'None'
    pipelineInfo_author_name = 'None'
    pipelineInfo_author_emailAdress = 'None'
    pipelineInfo_dateTime_creationDateTime = 'None'
    pipelineInfo_dateTime_modificationDateTime = 'None'
    pipelineInfo_uuid = 'None'
    pipelineInfo_systemVersion_majorVersion = 'None'
    pipelineInfo_systemVersion_minorVersion = 'None'
    pipelineInfo_systemVersion_patchVersion = 'None'

    #inputTransform部分
    inputTransform_applied = 'None'
    inputTransform_description = 'None'
    inputTransform_hash = 'None'
    inputTransform_uuid = 'None'
    inputTransform_file = 'None'
    inputTransform_transformId = 'None'

    inverseOutputTransform_description = 'None'
    inverseOutputTransform_hash = 'None'
    inverseOutputTransform_uuid = 'None'
    inverseOutputTransform_file = 'None'
    inverseOutputTransform_transformId = 'None'

    inverseOutputDeviceTransform_description = 'None'
    inverseOutputDeviceTransform_hash = 'None'
    inverseOutputDeviceTransform_uuid = 'None'
    inverseOutputDeviceTransform_file = 'None'
    inverseOutputDeviceTransform_transformId = 'None'

    inverseReferenceRenderingTransform_description = 'None'
    inverseReferenceRenderingTransform_hash = 'None'
    inverseReferenceRenderingTransform_uuid = 'None'
    inverseReferenceRenderingTransform_file = 'None'
    inverseReferenceRenderingTransform_transformId = 'None'

    #LMT部分
    lookTransform_applied = 'None'
    lookTransform_description = 'None'
    lookTransform_hash = 'None'
    lookTransform_uuid = 'None'
    lookTransform_file = 'None'
    lookTransform_transformId = 'None'

    cdlWorkingSpace_toCdlWorkingSpace_description = 'None'
    cdlWorkingSpace_toCdlWorkingSpace_hash = 'None'
    cdlWorkingSpace_toCdlWorkingSpace_uuid = 'None'
    cdlWorkingSpace_toCdlWorkingSpace_file = 'None'
    cdlWorkingSpace_toCdlWorkingSpace_transformId = 'None'

    cdlWorkingSpace_fromCdlWorkingSpace_description = 'None'
    cdlWorkingSpace_fromCdlWorkingSpace_hash = 'None'
    cdlWorkingSpace_fromCdlWorkingSpace_uuid = 'None'
    cdlWorkingSpace_fromCdlWorkingSpace_file = 'None'
    cdlWorkingSpace_fromCdlWorkingSpace_transformId = 'None'

    ASC_SOP_Slope = 'None'
    ASC_SOP_Offset = 'None'
    ASC_SOP_Power = 'None'
    ASC_SAT_Saturation = 'None'
    ColorCorrectionRef_ref = 'None'
    ColorCorrectionRef_Description = 'None'

    # outputTransform部分
    outputTransform_description = 'None'
    outputTransform_hash = 'None'
    outputTransform_uuid = 'None'
    outputTransform_file = 'None'
    outputTransform_transformId = 'None'

    outputDeviceTransform_description = 'None'
    outputDeviceTransform_hash = 'None'
    outputDeviceTransform_uuid = 'None'
    outputDeviceTransform_file = 'None'
    outputDeviceTransform_transformId = 'None'

    referenceRenderingTransform_description = 'None'
    referenceRenderingTransform_hash = 'None'
    referenceRenderingTransform_uuid = 'None'
    referenceRenderingTransform_file = 'None'
    referenceRenderingTransform_transformId = 'None'


    # 找到root节点下的所有pipeline节点
    for pipeline in root.findall(aces_amfVersionNumber+'pipeline'):

        # 查找pipeline节点下的 pipelineInfo 节点下的内容
        for pipelineInfo in pipeline.iter(aces_amfVersionNumber + 'pipelineInfo'):
            #查找description
            pipelineInfo_description = pipelineInfo.find(aces_amfVersionNumber + 'description')
            if pipelineInfo_description is not None:
                pipelineInfo_description = pipelineInfo_description.text
            #查找author节点下的内容
            for author in pipelineInfo.iter(aces_amfVersionNumber + 'author'):
                pipelineInfo_author_name = author.find(aces_amfVersionNumber + 'name')
                if pipelineInfo_author_name is not None:
                    pipelineInfo_author_name = pipelineInfo_author_name.text
                pipelineInfo_author_emailAdress = author.find(aces_amfVersionNumber + 'emailAddress')
                if pipelineInfo_author_emailAdress is not None:
                    pipelineInfo_author_emailAdress = pipelineInfo_author_emailAdress.text
            # 查找dateTime节点下的内容
            for dateTime in pipelineInfo.iter(aces_amfVersionNumber + 'dateTime'):
                pipelineInfo_dateTime_creationDateTime = dateTime.find(aces_amfVersionNumber + 'creationDateTime')
                if pipelineInfo_dateTime_creationDateTime is not None:
                    pipelineInfo_dateTime_creationDateTime = pipelineInfo_dateTime_creationDateTime.text
                pipelineInfo_dateTime_modificationDateTime = dateTime.find(aces_amfVersionNumber + 'modificationDateTime')
                if pipelineInfo_dateTime_modificationDateTime is not None:
                    pipelineInfo_dateTime_modificationDateTime = pipelineInfo_dateTime_modificationDateTime.text
            #查找description
            uuid = pipelineInfo.find(aces_amfVersionNumber + 'uuid')
            if uuid is not None:
                pipelineInfo_uuid = uuid.text[9:]
            #查找systemVersion节点下的内容
            for systemVersion in pipelineInfo.iter(aces_amfVersionNumber + 'systemVersion'):
                pipelineInfo_systemVersion_majorVersion = systemVersion.find(aces_amfVersionNumber + 'majorVersion')
                if pipelineInfo_systemVersion_majorVersion is not None:
                    pipelineInfo_systemVersion_majorVersion = pipelineInfo_systemVersion_majorVersion.text
                pipelineInfo_systemVersion_minorVersion = systemVersion.find(aces_amfVersionNumber + 'minorVersion')
                if pipelineInfo_systemVersion_minorVersion is not None:
                    pipelineInfo_systemVersion_minorVersion = pipelineInfo_systemVersion_minorVersion.text
                pipelineInfo_systemVersion_patchVersion = systemVersion.find(aces_amfVersionNumber + 'patchVersion')
                if pipelineInfo_systemVersion_patchVersion is not None:
                    pipelineInfo_systemVersion_patchVersion = pipelineInfo_systemVersion_patchVersion.text


            # 查找 pipeline 节点下的 inputTransform 节点里的 applied 属性
            inputTransform = pipeline.find(aces_amfVersionNumber + 'inputTransform')
            inputTransform_applied = inputTransform.get('applied')
            if inputTransform_applied is not None:
                inputTransform_applied = inputTransform.get('applied')

            # 调取Pipeline下inputTransform的信息
            for inputTransform in pipeline.iter(aces_amfVersionNumber + 'inputTransform'):
                inputTransform_description,inputTransform_hash,inputTransform_uuid,inputTransform_file,inputTransform_transformId = TransformFunction('inputTransform',pipeline)
            # 调取inputTransform下inverseOutputTransform的信息
            for inverseOutputTransform in inputTransform.iter(aces_amfVersionNumber + 'inverseOutputTransform'):
                inverseOutputTransform_description, inverseOutputTransform_hash, inverseOutputTransform_uuid, inverseOutputTransform_file,inverseOutputTransform_transformId = TransformFunction('inverseOutputTransform',inputTransform)
            # 调取inputTransform下inverseOutputDeviceTransform的信息
            for inverseOutputDeviceTransform in inputTransform.iter(aces_amfVersionNumber + 'inverseOutputDeviceTransform'):
                inverseOutputDeviceTransform_description, inverseOutputDeviceTransform_hash, inverseOutputDeviceTransform_uuid, inverseOutputDeviceTransform_file,inverseOutputDeviceTransform_transformId = TransformFunction('inverseOutputTransform', inputTransform)
            # 调取inputTransform下inverseReferenceRenderingTransform的信息
            for inverseReferenceRenderingTransform in inputTransform.iter(aces_amfVersionNumber + 'inverseReferenceRenderingTransform'):
                inverseReferenceRenderingTransform_description, inverseReferenceRenderingTransform_hash, inverseReferenceRenderingTransform_uuid, inverseReferenceRenderingTransform_file,inverseReferenceRenderingTransform_transformId = TransformFunction('inverseReferenceRenderingTransform',inputTransform)



            # 查找 pipeline 节点下的 lookTransform 节点里的 applied 属性
            lookTransform = pipeline.find(aces_amfVersionNumber + 'lookTransform')
            if lookTransform is not None:
                lookTransform_applied = lookTransform.get('applied')
            ColorCorrectionRef_ref = lookTransform.find(cdl_VersionNumber + 'ColorCorrectionRef')
            if ColorCorrectionRef_ref is not None:
                ColorCorrectionRef_ref = ColorCorrectionRef_ref.get('ref')
            #    ColorCorrectionRef_Description = ColorCorrectionRef_ref.find("{urn:ASC:CDL:v1.01}" + 'Description')
            #    print(ColorCorrectionRef_Description)
            #    if ColorCorrectionRef_Description is not None:
            #        ColorCorrectionRef_Description = ColorCorrectionRef_Description.text


            # 查找lookTransform下SOPNode里Slope、Offset、Power三个参数的信息
            for SOPNode in lookTransform.iter(cdl_VersionNumber + 'SOPNode'):
                if SOPNode is not None:
                    ASC_SOP_Slope = SOPNode.find(cdl_VersionNumber + 'Slope')
                    ASC_SOP_Offset = SOPNode.find(cdl_VersionNumber + 'Offset')
                    ASC_SOP_Power = SOPNode.find(cdl_VersionNumber + 'Power')
                    if ASC_SOP_Slope is not None:
                        ASC_SOP_Slope = ASC_SOP_Slope.text
                    if ASC_SOP_Offset is not None:
                        ASC_SOP_Offset = ASC_SOP_Offset.text
                    if ASC_SOP_Power is not None:
                        ASC_SOP_Power = ASC_SOP_Power.text
            # 查找lookTransform下SOPNode里Saturation的信息
            for SatNode in lookTransform.iter(cdl_VersionNumber + 'SatNode'):
                if SatNode is not None:
                    ASC_SAT_Saturation = SatNode.find(cdl_VersionNumber + 'Saturation')
                    if ASC_SAT_Saturation is not None:
                        ASC_SAT_Saturation = ASC_SAT_Saturation.text


            # 调取Pipeline下的lookTransform的信息
            for lookTransform in pipeline.iter(aces_amfVersionNumber + 'lookTransform'):
                lookTransform_description,lookTransform_hash,lookTransform_uuid,lookTransform_file,lookTransform_transformId = TransformFunction('lookTransform',pipeline)
            # 调取cdlWorkingSpace下的toCdlWorkingSpace的信息
            for cdlWorkingSpace in pipeline.iter(aces_amfVersionNumber + 'cdlWorkingSpace'):
                for toCdlWorkingSpace in cdlWorkingSpace.iter(aces_amfVersionNumber + 'toCdlWorkingSpace'):
                    cdlWorkingSpace_toCdlWorkingSpace_description,cdlWorkingSpace_toCdlWorkingSpace_hash,cdlWorkingSpace_toCdlWorkingSpace_uuid,cdlWorkingSpace_toCdlWorkingSpace_file,cdlWorkingSpace_toCdlWorkingSpace_transformId = TransformFunction('toCdlWorkingSpace',cdlWorkingSpace)
                # 调取cdlWorkingSpace下的fromCdlWorkingSpace的信息
                for fromCdlWorkingSpace in cdlWorkingSpace.iter(aces_amfVersionNumber + 'fromCdlWorkingSpace'):
                    cdlWorkingSpace_fromCdlWorkingSpace_description,cdlWorkingSpace_fromCdlWorkingSpace_hash,cdlWorkingSpace_fromCdlWorkingSpace_uuid,cdlWorkingSpace_fromCdlWorkingSpace_file,cdlWorkingSpace_fromCdlWorkingSpace_transformId = TransformFunction('fromCdlWorkingSpace',cdlWorkingSpace)


            # 调取Pipeline下outputTransform的信息
            for outputTransform in pipeline.iter(aces_amfVersionNumber + 'outputTransform'):
                outputTransform_description,outputTransform_hash,outputTransform_uuid,outputTransform_file,outputTransform_transformId = TransformFunction('outputTransform',pipeline)
            # 调取putTransform下outputDeviceTransform的信息
            for outputDeviceTransform in outputTransform.iter(aces_amfVersionNumber + 'outputDeviceTransform'):
                outputDeviceTransform_description, outputDeviceTransform_hash, outputDeviceTransform_uuid, outputDeviceTransform_file,outputDeviceTransform_transformId = TransformFunction('outputDeviceTransform',outputTransform)
            # 调取putTransform下referenceRenderingTransform的信息
            for referenceRenderingTransform in outputTransform.iter(aces_amfVersionNumber + 'referenceRenderingTransform'):
                referenceRenderingTransform_description, referenceRenderingTransform_hash, referenceRenderingTransform_uuid, referenceRenderingTransform_file,referenceRenderingTransform_transformId = TransformFunction('referenceRenderingTransform',outputTransform)


    pipeline1_rst['description']=pipelineInfo_description
    pipeline1_rst['author_name']=pipelineInfo_author_name
    pipeline1_rst['author_emailAdress']=pipelineInfo_author_emailAdress
    pipeline1_rst['dateTime_creationDateTime']=pipelineInfo_dateTime_creationDateTime
    pipeline1_rst['dateTime_modificationDateTime']=pipelineInfo_dateTime_modificationDateTime
    pipeline1_rst['uuid']=pipelineInfo_uuid
    pipeline1_rst['systemVersion_majorVersion']=pipelineInfo_systemVersion_majorVersion
    pipeline1_rst['systemVersion_minorVersion'] = pipelineInfo_systemVersion_minorVersion
    pipeline1_rst['systemVersion_patchVersion'] = pipelineInfo_systemVersion_patchVersion

    pipeline1_rst['inputTransform_applied']=inputTransform_applied
    pipeline1_rst['inputTransform_description']=inputTransform_description
    pipeline1_rst['inputTransform_hash']=inputTransform_hash
    pipeline1_rst['inputTransform_uuid']=inputTransform_uuid
    pipeline1_rst['inputTransform_file']=inputTransform_file
    pipeline1_rst['inputTransform_transformId']=inputTransform_transformId

    pipeline1_rst['inverseOutputTransform_description']=inverseOutputTransform_description
    pipeline1_rst['inverseOutputTransform_hash']=inverseOutputTransform_hash
    pipeline1_rst['inverseOutputTransform_uuid']=inverseOutputTransform_uuid
    pipeline1_rst['inverseOutputTransform_file']=inverseOutputTransform_file
    pipeline1_rst['inverseOutputTransform_transformId']=inverseOutputTransform_transformId

    pipeline1_rst['inverseOutputDeviceTransform_description']=inverseOutputDeviceTransform_description
    pipeline1_rst['inverseOutputDeviceTransform_hash']=inverseOutputDeviceTransform_hash
    pipeline1_rst['inverseOutputDeviceTransform_uuid']=inverseOutputDeviceTransform_uuid
    pipeline1_rst['inverseOutputDeviceTransform_file']=inverseOutputDeviceTransform_file
    pipeline1_rst['inverseOutputDeviceTransform_transformId']=inverseOutputDeviceTransform_transformId

    pipeline1_rst['inverseReferenceRenderingTransform_description']=inverseReferenceRenderingTransform_description
    pipeline1_rst['inverseReferenceRenderingTransform_hash']=inverseReferenceRenderingTransform_hash
    pipeline1_rst['inverseReferenceRenderingTransform_uuid']=inverseReferenceRenderingTransform_uuid
    pipeline1_rst['inverseReferenceRenderingTransform_file']=inverseReferenceRenderingTransform_file
    pipeline1_rst['inverseReferenceRenderingTransform_transformId']=inverseReferenceRenderingTransform_transformId

    pipeline1_rst['lookTransform_applied'] = lookTransform_applied
    pipeline1_rst['lookTransform_description']=lookTransform_description
    pipeline1_rst['lookTransform_hash']=lookTransform_hash
    pipeline1_rst['lookTransform_uuid']=lookTransform_uuid
    pipeline1_rst['lookTransform_file']=lookTransform_file
    pipeline1_rst['lookTransform_transformId']=lookTransform_transformId

    pipeline1_rst['cdlWorkingSpace_toCdlWorkingSpace_description'] = cdlWorkingSpace_toCdlWorkingSpace_description
    pipeline1_rst['cdlWorkingSpace_toCdlWorkingSpace_hash'] = cdlWorkingSpace_toCdlWorkingSpace_hash
    pipeline1_rst['cdlWorkingSpace_toCdlWorkingSpace_uuid'] = cdlWorkingSpace_toCdlWorkingSpace_uuid
    pipeline1_rst['cdlWorkingSpace_toCdlWorkingSpace_file'] = cdlWorkingSpace_toCdlWorkingSpace_file
    pipeline1_rst['cdlWorkingSpace_toCdlWorkingSpace_transformId'] = cdlWorkingSpace_toCdlWorkingSpace_transformId

    pipeline1_rst['cdlWorkingSpace_fromCdlWorkingSpace_description'] = cdlWorkingSpace_fromCdlWorkingSpace_description
    pipeline1_rst['cdlWorkingSpace_fromCdlWorkingSpace_hash'] = cdlWorkingSpace_fromCdlWorkingSpace_hash
    pipeline1_rst['cdlWorkingSpace_fromCdlWorkingSpace_uuid'] = cdlWorkingSpace_fromCdlWorkingSpace_uuid
    pipeline1_rst['cdlWorkingSpace_fromCdlWorkingSpace_file'] = cdlWorkingSpace_fromCdlWorkingSpace_file
    pipeline1_rst['cdlWorkingSpace_fromCdlWorkingSpace_transformId'] = cdlWorkingSpace_fromCdlWorkingSpace_transformId

    pipeline1_rst['ASC_SOP_Slope'] = ASC_SOP_Slope
    pipeline1_rst['ASC_SOP_Offset'] = ASC_SOP_Offset
    pipeline1_rst['ASC_SOP_Power'] = ASC_SOP_Power
    pipeline1_rst['ASC_SAT_Saturation'] = ASC_SAT_Saturation
    pipeline1_rst['ColorCorrectionRef_ref'] = ColorCorrectionRef_ref
    pipeline1_rst['ColorCorrectionRef_Description'] = ColorCorrectionRef_Description

    pipeline1_rst['outputTransform_description']=outputTransform_description
    pipeline1_rst['outputTransform_hash']=outputTransform_hash
    pipeline1_rst['outputTransform_uuid']=outputTransform_uuid
    pipeline1_rst['outputTransform_file']=outputTransform_file
    pipeline1_rst['outputTransform_transformId']=outputTransform_transformId

    pipeline1_rst['outputDeviceTransform_description']=outputDeviceTransform_description
    pipeline1_rst['outputDeviceTransform_hash']=outputDeviceTransform_hash
    pipeline1_rst['outputDeviceTransform_uuid']=outputDeviceTransform_uuid
    pipeline1_rst['outputDeviceTransform_file']=outputDeviceTransform_file
    pipeline1_rst['outputDeviceTransform_transformId']=outputDeviceTransform_transformId

    pipeline1_rst['referenceRenderingTransform_description']=referenceRenderingTransform_description
    pipeline1_rst['referenceRenderingTransform_hash']=referenceRenderingTransform_hash
    pipeline1_rst['referenceRenderingTransform_uuid']=referenceRenderingTransform_uuid
    pipeline1_rst['referenceRenderingTransform_file']=referenceRenderingTransform_file
    pipeline1_rst['referenceRenderingTransform_transformId']=referenceRenderingTransform_transformId

    return pipeline1_rst