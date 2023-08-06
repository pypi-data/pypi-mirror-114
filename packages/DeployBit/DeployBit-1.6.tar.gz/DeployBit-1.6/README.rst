*****************
DeployBit
*****************
DeployBit - A New Door to Salesforce
---------------------------------------
DeployBit is Salesforce Metadata API based, Lightweight Python Environment to Smoothen and Support your Development and Deployment Processes.


Supported API Calls
--------------------------
- ``Login``
- ``Deploy``
- ``Check Deploy Status``
- ``Cancel Deploy``
- ``Retrieve``
- ``Check Retrieve Status``
- ``Describe Metadata``
- ``List Metadata``
- ``Query``
- ``Query More``
- ``Search``
- ``Apex Execute``
- ``Logout``

Examples
--------------------------

``1. DeployBitSalesforce Constructor - DeployBitSalesforce(username,password,security_token,session_id,api_version,environment)``

  DeployBitSalesforce constructor returns us the object to be used for salesforce connection, when provided with below details.

- ``username`` - Username of the salesforce org  
- ``password`` - Password of the salesforce org  
- ``security_token`` - Security Token of the salesforce org  
- ``session_id`` - Session Id of the salesforce org  
- ``api_version`` - Api Version of the salesforce org  eg. ``45.0``, default value is ``50.0``
- ``environment`` - Environment of the salesforce org  eg. ``login`` for Production org and ``test`` for sandbox, default value is ``login``

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','aksdhjhasdas5d6asdhjasgdhasrd5a354sd678asd','45.0','test')
  
------


``2. Login - login()``

  This method establishes connection to salesforce using details provided to DeployBitSalesforce constructor if credentials are correct and returns `LoginResult <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_login_loginresult.htm#topic-title>`__.


For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123',None,'45.0','test')
    sf.login()

------

``3. Deploy - deploy(zip_file_path,**deploy_options)``

 This method deploys provided package ``.zip`` and returns deployment/validation status details using given `DeployOptions <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm>`__.
 
- ``zip_file_path`` - File path for .zip to be deployed
- ``checkOnly`` - Flag decides type of deployment eg. ``Deployment`` or ``Validation``
- ``testLevel`` - This attributes decides the level of the test execustion eg. ``RunSpecifiedTests`` , ``NoTestRun``   
- ``runTests`` - A list of Apex classes containing tests run after deployment when ``RunSpecifiedTests``
- ``ignoreWarnings`` - This setting indicates that a deployment succeeds even if there are warnings (true)
- ``allowMissingFiles`` - Specifies whether a deploy succeeds even if files that are specified in package.xml are not in the zip file.
- ``autoUpdatePackage`` - Specifies whether a deploy continues even if files present in the zip file are not specified in package.xml.
- ``performRetrieve`` - Specifies whether a deploy continues even if files present in the zip file are not specified in package.xml.
- ``purgeOnDelete`` - If true, the deleted components in the destructiveChanges.xml manifest file aren't stored in the Recycle Bin.
- ``rollbackOnError`` - Indicates whether any failure causes a complete rollback (true) or not (false).
- ``singlePackage`` - Declares that the zipFile or deployRoot parameter points to a directory structure with a single package, as opposed to a set of packages.


For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    deploy_result=sf.deploy("/Documents/Release/TestClassPackage.zip",checkOnly=True,singlePackage=True,testLevel='runspecifiedtests',runTests=['DummyClasstest'])
    
--------

``4. Check Deploy Status - check_deploy_status(deployment_id,include_details)``

 This method checks current deployment status using provided ``deployment_id``, ``include_details`` as ``True`` and returns deployment/validation details using `DeployResult <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deployresult.htm>`__.
 

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    deploy_result=sf.check_deploy_status('DeploymentId',include_details=True)

--------

``5. Cancel Deploy - cancel_deploy(deployment_id)``

 This method cancels ongoing deployment using provided ``deployment_id``.
 

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    deploy_result=sf.cancel_deploy('DeploymentId')
    
----------

``6. Retrieve - retrieve(xml_file_path,single_package)``

 This method initiates retrieve request for all mentioned components in the package.xml path provided in ``xml_file_path`` and returns ``retrieve_id`` to be used to get package data. Package behaviour will be based on ``single_package`` flag.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    retrieve_result=sf.retrieve("/Documents/Release/download.xml",single_package=True)
 
----------

``7. Check Retrieve Status - check_retrieve_status(retrieve_id,include_zip)``

 This method returns initiated retrieve request status using provided ``retrieve_id`` and returns `RetrieveResult <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_retrieveresult.htm>`__ containing ``base64 zip string`` to be used for zip package generation if ``include_zip`` option is marked to ``True``.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    import base64,os
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    retrieve_result=sf.check_retrieve_status('RetrieveId',include_zip=True)
    currentDirectory='/Documents/Release'
    with open(os.path.join(currentDirectory,'output_file.zip'), 'wb') as result:
            result.write(base64.b64decode(retrieve_result['zipFile']))
            
----------

``8. Describe Metadata - describe_metadata()``

 This method uses provided ``api_version`` in DeployBitSalesforce object and retrieves the metadata that describes your organization using `DescribeMetadataResult <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_describemeta_result.htm>`__.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    describe_result=sf.describe_metadata()

----------

``9. List Metadata - list_metadata(metadata_type)``

 This method retrieves property information about metadata components in your organization using provided ``metadata_type`` and ``api_version`` in DeployBitSalesforce object, returns `FileProperties <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_retrieveresult.htm#retrieveresult_fileproperties>`__.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    describe_result=sf.list_metadata('ApexClass')

----------

``10. Query - query(query_string,batch_size,is_tooling_api)``

 This method executes a query against the specified object and returns data that matches the specified criteria using `QueryResult <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_query_queryresult.htm#topic-title>`__.
 
- ``query_string`` - A ``SOQL`` string to be used for query eg. ``SELECT id from Account limit 100``
- ``batch_size`` - Chunk size of the results to be returned from total records.
- ``is_tooling_api`` - ``True`` will enable tooling API eg. ``SELECT id from CustomObject``

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    query_result=sf.query("Select Id from Account",batch_size=250)

----------

``11. Query More - query_more(query_locator,batch_size,is_tooling_api)``

 This method retrieves the next batch of objects from a query() and returns data using `QueryResult <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_query_queryresult.htm#topic-title>`__.
 
- ``query_locator`` - A ``query_locator`` id returned by ``query()`` call in QueryResult
- ``batch_size`` - Chunk size of the results to be returned from total records.
- ``is_tooling_api`` - ``True`` will enable tooling API eg. ``SELECT id from CustomObject``

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    query_result=sf.query_more("QueryLocatorId",batch_size=250)

----------

``12. Search - search(search_string,is_tooling_api)``

 This method retrieves the next batch of objects from a query() and returns data using `SearchResult <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_search_searchresult.htm#topic-title>`__.
 
- ``search_string`` - A ``SOSL`` string to be used for search eg. ``FIND {Test*} IN ALL FIELDS RETURNING Account(Name)``
- ``is_tooling_api`` - ``True`` will enable tooling API eg. ``FIND {Test*} in all fields returning CustomObject(Id,ManageableState)``

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    search_result=sf.search("FIND {Test*} IN ALL FIELDS RETURNING Account(Name)")
    
-----------

``13. Apex Execute - apex_execute(code_chunk,log_category,log_category_level)``

 This method compiles, executes your apex code chunks and returns results/debugs details using `ExecuteAnonymousResult <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_executeanonymous_result.htm#topic-title>`__ based on ``log_category`` and ``log_category_level`` options availble here `DebuggingHeader <https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_header_debuggingheader.htm>`__.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    debugString="""List<Account> accList=[select Id,Name from Account limit 10];
                for(Account acc:accList)
                {
                  System.debug('===acc==='+acc.Name);    
                }"""
    execute_result=sf.apex_execute(debugString)
 
-----------

``14. Logout - logout()``

 This method terminates your session. New session can be created using ``login()`` method.

For example:

.. code-block:: python

    from DeployBit import DeployBitSalesforce
    sf=DeployBitSalesforce('test@test.com','test123','tEstTesting123','45.0','test')
    sf.login()
    search_result=sf.search("FIND {Test*} IN ALL FIELDS RETURNING Account(Name)")
    sf.logout()

Other DeployBit Implementations
-----------------------------------

  - `DeployBit Salesforce(LWC) <https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FR5S9UAL>`__
  - `DeployBit Android <https://play.google.com/store/apps/details?id=com.deploybit.deploybit>`__

Author
--------------------------

   DeployBit is written by Padmnabh Munde.




