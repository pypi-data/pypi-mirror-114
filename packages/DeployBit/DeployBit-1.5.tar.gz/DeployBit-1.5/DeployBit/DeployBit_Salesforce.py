
import requests
from DeployBit.DeployBit_Utility import *
from xml.sax.saxutils import escape

class DeployBitSalesforce:

    def __init__(this,
                username=None,
                password=None,
                security_token=None,
                session_id=None,
                api_version=DEFAULT_API_VERSION,
                environment=DEFAULT_ENVIRONMENT,
                ):
        this.username=username
        this.password=password
        this.security_token=security_token
        this.api_version=api_version
        this.environment=environment
        this.session=requests.session()
        this.session_id=session_id
        this.instance_url=None
    
    def login(this):
        if all((arg is None or arg=='') for arg in (this.username,this.password,this.security_token)):
            raise DeployBitLoginError('Please provide Username, Password, Security Token')
        else:
            soap_url = SOAP_URL.format(environment=this.environment,api_version=this.api_version)
            login_payload_attributes={'username':this.username, 
                                    'password':this.password, 
                                    'token':this.security_token}
            login_request = LOGIN_PAYLOAD.format(**login_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='login'
            login_response = call_http_salesforce(url=soap_url,
                                 method='POST',
                                 session=this.session,
                                 headers=REQUEST_HEADERS,
                                 data=login_request)
            login_result=process_login_response(login_response)
            this.session_id=login_result['sessionId']
            this.instance_url=(login_result['serverUrl']
                            .replace('http://', '')
                            .replace('https://', '')
                            .split('/')[0]
                            .replace('-api', ''))
            return login_result   

    def deploy(this,zip_file_path=None,**deploy_options):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling deploy()')
        elif zip_file_path is None:
            raise DeployBitDeploymentError('Please provide \'zip_file_path\' of .zip file')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            deploy_payload_attributes=get_deploy_attributes(this.session_id,zip_file_path,**deploy_options)
            deploy_request = DEPLOY_PAYLOAD.format(**deploy_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='deploy'
            deploy_response = call_http_salesforce(url=metadata_url,
                                        method='POST',
                                        session=this.session,
                                        headers=REQUEST_HEADERS,
                                        data=deploy_request)
            deploy_result=process_deploy_response(deploy_response)
            return deploy_result
    
    def check_deploy_status(this,deployment_id,include_details='false'):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling check_deploy_status()')
        elif deployment_id is None and deployment_id!='':
            raise DeployBitDeploymentError('Please provide deployment id to proceed')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            check_deploy_payload_attributes = {
            'sessionId': this.session_id,
            'deploymentId': deployment_id,
            'includeDetails': include_details
            }
            check_deploy_request = CHECK_DEPLOY_PAYLOAD.format(**check_deploy_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='checkDeployStatus'
            check_deploy_response = call_http_salesforce(
                            url=metadata_url,
                            method='POST',
                            session=this.session,
                            headers=REQUEST_HEADERS,
                            data=check_deploy_request)
            check_deploy_result=process_check_deploy_response(check_deploy_response)
        
            return check_deploy_result
    
    def cancel_deploy(this,deployment_id):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling cancel_deploy()')
        elif deployment_id is None and deployment_id!='':
            raise DeployBitDeploymentError('Please provide deployment id to proceed')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            cancel_deploy_payload_attributes = {
            'sessionId': this.session_id,
            'deploymentId': deployment_id,
            }
            cancel_deploy_request = CANCEL_DEPLOY_PAYLOAD.format(**cancel_deploy_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='cancelDeploy' 
            
            cancel_deploy_response = call_http_salesforce(
                url=metadata_url,
                method='POST',
                session=this.session,
                headers=REQUEST_HEADERS,
                data=cancel_deploy_request)
            cancel_deploy_result=process_cancel_deploy_response(cancel_deploy_response)
            return cancel_deploy_result

    def retrieve(this,xml_file_path,single_package=True):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling retrieve()')
        elif xml_file_path is None and xml_file_path!='':
            raise DeployBitRetrieveError('Please provide xml_file_path to proceed')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            retrieve_payload_attributes = {
            'retrievePackage': read_xml_from_path(xml_file_path),
            'sessionId': this.session_id,
            'apiVersion': this.api_version,
            'singlePackage': single_package,
            }
            retrieve_request = RETRIEVE_PAYLOAD.format(**retrieve_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='retrieve'    

            retrieve_response = call_http_salesforce(url=metadata_url,
                                    method='POST',
                                    session=this.session,
                                    headers=REQUEST_HEADERS,
                                    data=retrieve_request)                
            retrieve_result=process_retrieve_response(retrieve_response,'retrieveResponse')
            return retrieve_result

    def check_retrieve_status(this,retrieve_id=None,include_zip=False):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling check_retrieve_status()')
        elif retrieve_id is None and retrieve_id!='':
            raise DeployBitRetrieveError('Please provide retrieve_id to proceed')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version) 
            check_retrieve_payload_attributes = {
            'retrieveId': retrieve_id,
            'sessionId': this.session_id,
            'includeZip':include_zip
            }
            check_retrieve_request = CHECK_RETRIEVE_PAYLOAD.format(**check_retrieve_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='checkRetrieveStatus'
            check_retrieve_response = call_http_salesforce(url=metadata_url,
                                 method='POST',
                                 session=this.session,
                                 headers=REQUEST_HEADERS,
                                 data=check_retrieve_request)    
            retrieve_result=process_retrieve_response(check_retrieve_response,'checkRetrieveStatusResponse')
            return retrieve_result
        
    def describe_metadata(this):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling describe_metadata()')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            describe_metadata_payload_attributes = {
            'sessionId': this.session_id,
            'apiVersion':this.api_version
            }
            describe_metadata_request = DESCRIBE_TYPES_PAYLOAD.format(**describe_metadata_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='describeMetadata' 

            describe_metadata_response = call_http_salesforce(
                            url=metadata_url,
                            method='POST',
                            session=this.session,
                            headers=REQUEST_HEADERS,
                            data=describe_metadata_request)
            describe_metadata_result=process_describe_metadata_response(describe_metadata_response)
            return describe_metadata_result

    def list_metadata(this,metadata_type):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling list_metadata()')
        elif metadata_type is None and metadata_type!='':
            raise DeployBitListMetadataError('Please provide metadata type to proceed')
        else:
            metadata_url=METADATA_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            list_metadata_payload_attributes = {
                                        'sessionId': this.session_id,
                                        'apiVersion':this.api_version,
                                        'metadataType':metadata_type
                                        }
            list_metadata_request = LIST_METADATA_PAYLOAD.format(**list_metadata_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='listMetadata' 
            list_metadata_response = call_http_salesforce(
                                url=metadata_url,
                                method='POST',
                                session=this.session,
                                headers=REQUEST_HEADERS,
                                data=list_metadata_request)
            list_metadata_result=process_list_metadata_response(list_metadata_response)
            return list_metadata_result
        
    def query(this,query_string,batch_size=200,is_tooling_api=False):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling query()')
        elif query_string is None and query_string!='':
            raise DeployBitQueryError('Please enter SOQL query')
        else:
            query_url=QUERY_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            api_name='partner'
            if is_tooling_api:
                query_url=TOOLING_URL.format(instance_url=this.instance_url,api_version=this.api_version)
                api_name='tooling'
            
            query_payload_attributes = {
            'sessionId': this.session_id,
            'batchSize':batch_size,
            'queryString':query_string,
            'apiName':api_name
            }
            query_request = QUERY_PAYLOAD.format(**query_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='query'
            query_response = call_http_salesforce(
                url=query_url,
                method='POST',
                session=this.session,
                headers=REQUEST_HEADERS,
                data=query_request)
            query_result=process_query_response(query_response,'queryResponse',is_tooling_api)
            return query_result
    
    def query_more(this,query_locator,batch_size=200,is_tooling_api=False):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling query_more()')
        elif query_locator is None and query_locator!='':
            raise DeployBitQueryError('Please provide query locator to query more records')
        else:
            query_url=QUERY_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            api_name='partner'
            if is_tooling_api:
                query_url=TOOLING_URL.format(instance_url=this.instance_url,api_version=this.api_version)
                api_name='tooling'
            query_more_payload_attributes = {
            'sessionId': this.session_id,
            'batchSize':batch_size,
            'queryLocator':query_locator,
            'apiName':api_name
            }
            query_more_request = QUERY_MORE_PAYLOAD.format(**query_more_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='queryMore'

            query_more_response = call_http_salesforce(
                url=query_url,
                method='POST',
                session=this.session,
                headers=REQUEST_HEADERS,
                data=query_more_request)
            query_more_result=process_query_response(query_more_response,'queryMoreResponse')
            return query_more_result
    
    def search(this,search_string,is_tooling_api=False):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling query()')
        elif search_string is None and search_string!='':
            raise DeployBitQueryError('Please enter SOSL query')
        else:
            search_url=QUERY_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            api_name='partner'
            if is_tooling_api:
                search_url=TOOLING_URL.format(instance_url=this.instance_url,api_version=this.api_version)
                api_name='tooling'
            
            search_payload_attributes = {
            'sessionId': this.session_id,
            'searchString':search_string,
            'apiName':api_name
            }
            search_request = SEARCH_PAYLOAD.format(**search_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='search'
            search_response = call_http_salesforce(
                url=search_url,
                method='POST',
                session=this.session,
                headers=REQUEST_HEADERS,
                data=search_request)
            query_result=process_query_response(search_response,'searchResponse',is_tooling_api)
            return query_result
        
    def apex_execute(this,code_chunk,log_category='Apex_code',log_category_level='DEBUG'):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling apex_execute()')
        elif code_chunk is None and code_chunk!='':
            raise DeployBitQueryError('Please provide code snippet to execute')
        else:
            execute_url=APEX_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            
            apex_execute_payload_attributes = {
                                                'sessionId': this.session_id,
                                                'codeChunk':escape(code_chunk),
                                                'logCategory':log_category,
                                                'logCategoryLevel':log_category_level
                                            }
            apex_execute_request = APEX_EXECUTE_PAYLOAD.format(**apex_execute_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='executeAnonymous'
            apex_execute_response = call_http_salesforce(
                                url=execute_url,
                                method='POST',
                                session=this.session,
                                headers=REQUEST_HEADERS,
                                data=apex_execute_request)
            apex_execute_result=process_apex_execute_response(apex_execute_response)
            return apex_execute_result
    
    def logout(this):
        if all((arg is None or arg=='') for arg in (this.session_id,this.instance_url)):
            raise DeployBitLoginError('Please call login() method before calling deploy()')
        else:
            logout_url=QUERY_URL.format(instance_url=this.instance_url,api_version=this.api_version)
            logout_payload_attributes = {
                                        'sessionId': this.session_id
                                        }
            logout_request = LOGOUT_PAYLOAD.format(**logout_payload_attributes)
            REQUEST_HEADERS['SOAPAction']='logout'

            logout_response = call_http_salesforce(
                                                url=logout_url,
                                                method='POST',
                                                session=this.session,
                                                headers=REQUEST_HEADERS,
                                                data=logout_request)
            logout_result=process_logout_response(logout_response)
            return logout_result
        

    


