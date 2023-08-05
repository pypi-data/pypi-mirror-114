from DeployBit.DeployBit_Constants import *
from DeployBit.DeployBit_Exceptions import *
from xml.etree import ElementTree
from base64 import b64encode


def read_zip_from_path(zip_file):
    if hasattr(zip_file, 'read'):
        file = zip_file
        file.seek(0)
        should_close = False
    else:
        file = open(zip_file, 'rb')
        should_close = True
    raw = file.read()
    if should_close:
        file.close()
    return b64encode(raw).decode("utf-8")

def read_xml_from_path(xml_file):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    package_string=''
    for type in root.findall('mt:types',XML_NAMESPACES):
        package_string+='<met:types>\n'
        for member in type:
            field_name=member.tag
            field_name=field_name.replace(field_name[0:field_name.find("}")+1],"")
            if field_name=='members':
                package_string+='<met:members>'+str(member.text)+'</met:members>\n'
            elif field_name=='name':
                package_string+='<met:name>'+str(member.text)+'</met:name>\n'
        
        package_string+='</met:types>\n\n'
    return package_string

def get_deploy_attributes(session_id,zip_file_path,**deploy_options):
            deploy_payload_attributes = {
            'checkOnly': deploy_options.get('checkOnly', False),
            'sessionId': session_id,
            'zipFile': read_zip_from_path(zip_file_path),
            'testLevel': deploy_options.get('testLevel','NoTestRun'),
            'runTests': deploy_options.get('runTests'),
            'ignoreWarnings': deploy_options.get('ignoreWarnings', False),
            'allowMissingFiles': deploy_options.get('allowMissingFiles', False),
            'autoUpdatePackage': deploy_options.get('autoUpdatePackage', False),
            'performRetrieve': deploy_options.get('performRetrieve', False),
            'purgeOnDelete': deploy_options.get('purgeOnDelete', False),
            'rollbackOnError': deploy_options.get('rollbackOnError', False),
            'singlePackage': deploy_options.get('singlePackage', False),
            }
            
            run_tests_tag = ''
            testClassNames=deploy_payload_attributes['runTests']
            testLevel=deploy_payload_attributes['testLevel']
                
            if testClassNames and str(testLevel).lower() == 'runspecifiedtests':
                for test in testClassNames:
                    run_tests_tag += '<met:runTests>%s</met:runTests>\n' % test
                deploy_payload_attributes['runTests'] = run_tests_tag
            
            return deploy_payload_attributes

def call_http_salesforce(url, method, session, headers, **args):
    result = session.request(method, url, headers=headers, **args)
    return result

def get_exception_node(response):
    return ElementTree.fromstring(response.text).find(
                'soapenv:Body/soapenv:Fault',XML_NAMESPACES)

def process_exception_node(exception_node):
    return exception_node.find('faultstring',XML_NAMESPACES).text

def process_attribute_node(result):
    attributes={}
    for attribute in result:
        attribute_name=attribute.tag
        attribute_name=attribute_name.replace(attribute_name[0:attribute_name.find("}")+1],"")
        attribute_value=attribute.text
        if(len(attribute))>0:
            child_attributes=process_attribute_node(attribute)
            if attribute_name in attributes.keys():
                if type(attributes[attribute_name])==list:
                    temp_attribute_array=attributes[attribute_name]
                    temp_attribute_array.append(child_attributes)
                else:
                    temp_attribute_array=[attributes[attribute_name]]
                    temp_attribute_array.append(child_attributes)
                
                attributes[attribute_name]=temp_attribute_array
            else:
                if attribute_name in XML_ARRAY_TYPES:
                    attributes[attribute_name]=[child_attributes]
                else:
                    attributes[attribute_name]=child_attributes
        else:
            attributes[attribute_name]=attribute_value
    return attributes

def process_login_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitLoginError(fault_string)
    else:
        login_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/soap:loginResponse/soap:result',XML_NAMESPACES)
        return process_attribute_node(login_result)

def process_deploy_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitDeploymentError(fault_string)
    else:
        deploy_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:deployResponse/mt:result',XML_NAMESPACES)
        return process_attribute_node(deploy_result)

def process_check_deploy_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitDeploymentError(fault_string)
    else:
        check_deploy_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:checkDeployStatusResponse/mt:result',XML_NAMESPACES)
        return process_attribute_node(check_deploy_result)

def process_cancel_deploy_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitDeploymentError(fault_string)
    else:
        cancel_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:cancelDeployResponse/mt:result',XML_NAMESPACES)
        return process_attribute_node(cancel_result)

def process_retrieve_response(response,response_type):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitRetrieveError(fault_string)
    else:
        check_retrieve_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:'+str(response_type)+'/mt:result',XML_NAMESPACES)
        return process_attribute_node(check_retrieve_result)

def process_describe_metadata_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitDescribeMetadataError(fault_string)
    else:
        describe_metadata_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:describeMetadataResponse/mt:result',XML_NAMESPACES)
        return process_attribute_node(describe_metadata_result)

def process_list_metadata_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitListMetadataError(fault_string)
    else:
        list_metadata_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/mt:listMetadataResponse',XML_NAMESPACES)
        return process_attribute_node(list_metadata_result)

def process_query_response(response,response_type,is_tooling_api=False):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitQueryError(fault_string)
    else:
        query_result={}
        if is_tooling_api:
            query_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/tooling:'+str(response_type)+'/tooling:result',XML_NAMESPACES)
        else:
            query_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body/soap:'+str(response_type)+'/soap:result',XML_NAMESPACES)
            
        return process_attribute_node(query_result)

def process_apex_execute_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitApexExecuteError(fault_string)
    else:
        apex_execute_result=ElementTree.fromstring(response.text)
        return process_attribute_node(apex_execute_result)

def process_logout_response(response):
    exception_node=get_exception_node(response)
    if exception_node is not None:
        fault_string=process_exception_node(exception_node)
        raise DeployBitLogoutError(fault_string)
    else:
        logout_result=ElementTree.fromstring(response.text).find(
                'soapenv:Body',XML_NAMESPACES)
        return process_attribute_node(logout_result)



