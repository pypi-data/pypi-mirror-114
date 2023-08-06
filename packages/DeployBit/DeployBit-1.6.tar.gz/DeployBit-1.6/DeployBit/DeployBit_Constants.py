DEFAULT_API_VERSION='50.0'
DEFAULT_ENVIRONMENT='login'
XML_ARRAY_TYPES=['componentFailures','componentSuccesses','codeCoverage','codeCoverageWarnings','failures','flowCoverage','flowCoverageWarnings','successes','messages','fileProperties','metadataObjects','result','records','searchRecords']

SOAP_URL = 'https://{environment}.salesforce.com/services/Soap/u/{api_version}'
METADATA_URL ='https://{instance_url}/services/Soap/m/{api_version}'
QUERY_URL = 'https://{instance_url}/services/Soap/u/{api_version}'
APEX_URL = 'https://{instance_url}/services/Soap/s/{api_version}'
TOOLING_URL = 'https://{instance_url}/services/Soap/T/{api_version}'

REQUEST_HEADERS = {
                    'content-type': 'text/xml',
                    'charset': 'UTF-8',
                    'SOAPAction': 'SOAPAction'
                    }
XML_NAMESPACES = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'mt': 'http://soap.sforce.com/2006/04/metadata',
        'soap': 'urn:partner.soap.sforce.com',
        'apex': 'http://soap.sforce.com/2006/08/apex',
        'tooling':'urn:tooling.soap.sforce.com'
        }
LOGIN_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:urn="urn:partner.soap.sforce.com">
                    <soapenv:Body>
                        <urn:login>
                            <urn:username>{username}</urn:username>
                            <urn:password>{password}{token}</urn:password>
                        </urn:login>
                    </soapenv:Body>
                </soapenv:Envelope>"""

DEPLOY_PAYLOAD="""<soapenv:Envelope
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:met="http://soap.sforce.com/2006/04/metadata">
                <soapenv:Header>
                    <met:SessionHeader>
                        <met:sessionId>{sessionId}</met:sessionId>
                    </met:SessionHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <met:deploy>
                        <met:ZipFile>{zipFile}</met:ZipFile>
                        <met:DeployOptions>
                            <met:allowMissingFiles>{allowMissingFiles}</met:allowMissingFiles>
                            <met:autoUpdatePackage>{autoUpdatePackage}</met:autoUpdatePackage>
                            <met:checkOnly>{checkOnly}</met:checkOnly>
                            <met:ignoreWarnings>{ignoreWarnings}</met:ignoreWarnings>
                            <met:performRetrieve>{performRetrieve}</met:performRetrieve>
                            <met:purgeOnDelete>{purgeOnDelete}</met:purgeOnDelete>
                            <met:rollbackOnError>{rollbackOnError}</met:rollbackOnError>
                            <met:singlePackage>{singlePackage}</met:singlePackage>
                            <met:testLevel>{testLevel}</met:testLevel>
                            {runTests}
                        </met:DeployOptions>
                    </met:deploy>
                </soapenv:Body>
                </soapenv:Envelope>"""

CHECK_DEPLOY_PAYLOAD="""<soapenv:Envelope
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:met="http://soap.sforce.com/2006/04/metadata">
                    <soapenv:Header>
                        <met:SessionHeader>
                            <met:sessionId>{sessionId}</met:sessionId>
                        </met:SessionHeader>
                    </soapenv:Header>
                    <soapenv:Body>
                        <met:checkDeployStatus>
                            <met:asyncProcessId>{deploymentId}</met:asyncProcessId>
                            <met:includeDetails>{includeDetails}</met:includeDetails>
                        </met:checkDeployStatus>
                    </soapenv:Body>
                    </soapenv:Envelope>"""

CANCEL_DEPLOY_PAYLOAD="""<soapenv:Envelope 
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:met="http://soap.sforce.com/2006/04/metadata">
                        <soapenv:Header>
                            <met:SessionHeader>
                                <met:sessionId>{sessionId}</met:sessionId>
                            </met:SessionHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <met:cancelDeploy>
                                <met:String>{deploymentId}</met:String>
                            </met:cancelDeploy>
                        </soapenv:Body>
                        </soapenv:Envelope>"""

DESCRIBE_TYPES_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:met="http://soap.sforce.com/2006/04/metadata">
                    <soapenv:Header>
                        <met:SessionHeader>
                            <met:sessionId>{sessionId}</met:sessionId>
                        </met:SessionHeader>
                    </soapenv:Header>
                    <soapenv:Body>
                        <met:describeMetadata>
                            <met:asOfVersion>{apiVersion}</met:asOfVersion>
                        </met:describeMetadata>
                    </soapenv:Body>
                    </soapenv:Envelope>"""

LIST_METADATA_PAYLOAD="""<soapenv:Envelope 
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:met="http://soap.sforce.com/2006/04/metadata">
                        <soapenv:Header>
                            <met:SessionHeader>
                                <met:sessionId>{sessionId}</met:sessionId>
                            </met:SessionHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <met:listMetadata>
                                <met:queries>
                                    <met:type>{metadataType}</met:type>
                                </met:queries>
                                <met:asOfVersion>{apiVersion}</met:asOfVersion>
                            </met:listMetadata>
                        </soapenv:Body>
                        </soapenv:Envelope>"""

QUERY_PAYLOAD="""<soapenv:Envelope 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:urn="urn:{apiName}.soap.sforce.com">
                <soapenv:Header>
                    <urn:QueryOptions>
                        <urn:batchSize>{batchSize}</urn:batchSize>
                    </urn:QueryOptions>
                    <urn:SessionHeader>
                        <urn:sessionId>{sessionId}</urn:sessionId>
                    </urn:SessionHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <urn:query>
                        <urn:queryString>{queryString}</urn:queryString>
                    </urn:query>
                </soapenv:Body>
                </soapenv:Envelope>"""

QUERY_MORE_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:urn="urn:{apiName}.soap.sforce.com">
                        <soapenv:Header>
                            <urn:QueryOptions>
                                <urn:batchSize>{batchSize}</urn:batchSize>
                            </urn:QueryOptions>
                            <urn:SessionHeader>
                                <urn:sessionId>{sessionId}</urn:sessionId>
                            </urn:SessionHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <urn:queryMore>
                                <urn:queryLocator>{queryLocator}</urn:queryLocator>
                            </urn:queryMore>
                        </soapenv:Body>
                        </soapenv:Envelope>"""
SEARCH_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:urn="urn:{apiName}.soap.sforce.com">
                    <soapenv:Header>
                        <urn:SessionHeader>
                            <urn:sessionId>{sessionId}</urn:sessionId>
                        </urn:SessionHeader>
                    </soapenv:Header>
                    <soapenv:Body>
                        <urn:search>
                            <urn:queryString>{searchString}</urn:queryString>
                        </urn:search>
                    </soapenv:Body>
                    </soapenv:Envelope>"""
APEX_EXECUTE_PAYLOAD="""<soapenv:Envelope 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:apex="http://soap.sforce.com/2006/08/apex">
                <soapenv:Header>
                    <apex:DebuggingHeader>
                    <apex:categories>
                        <apex:category>{logCategory}</apex:category>
                        <apex:level>{logCategoryLevel}</apex:level>
                    </apex:categories>
                    </apex:DebuggingHeader>
                    <apex:SessionHeader>
                        <apex:sessionId>{sessionId}</apex:sessionId>
                    </apex:SessionHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <apex:executeAnonymous>
                        <apex:String>{codeChunk}</apex:String>
                    </apex:executeAnonymous>
                </soapenv:Body>
                </soapenv:Envelope>"""

LOGOUT_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:urn="urn:partner.soap.sforce.com">
                    <soapenv:Header>
                        <urn:SessionHeader>
                            <urn:sessionId>{sessionId}</urn:sessionId>
                        </urn:SessionHeader>
                    </soapenv:Header>
                    <soapenv:Body>
                        <urn:logout/>
                    </soapenv:Body>
                    </soapenv:Envelope>"""
RETRIEVE_PAYLOAD="""<soapenv:Envelope 
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:met="http://soap.sforce.com/2006/04/metadata">
                    <soapenv:Header>
                        <met:SessionHeader>
                            <met:sessionId>{sessionId}</met:sessionId>
                        </met:SessionHeader>
                    </soapenv:Header>
                    <soapenv:Body>
                        <met:retrieve>
                            <met:retrieveRequest>
                                <met:apiVersion>{apiVersion}</met:apiVersion>
                                <met:singlePackage>{singlePackage}</met:singlePackage>
                                <met:unpackaged>
                                {retrievePackage}
                                </met:unpackaged>
                            </met:retrieveRequest>
                        </met:retrieve>
                    </soapenv:Body>
                    </soapenv:Envelope>"""

CHECK_RETRIEVE_PAYLOAD="""<soapenv:Envelope 
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:met="http://soap.sforce.com/2006/04/metadata">
                        <soapenv:Header>
                            <met:SessionHeader>
                                <met:sessionId>{sessionId}</met:sessionId>
                            </met:SessionHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <met:checkRetrieveStatus>
                                <met:asyncProcessId>{retrieveId}</met:asyncProcessId>
                                <met:includeZip>{includeZip}</met:includeZip>
                            </met:checkRetrieveStatus>
                        </soapenv:Body>
                        </soapenv:Envelope>"""

