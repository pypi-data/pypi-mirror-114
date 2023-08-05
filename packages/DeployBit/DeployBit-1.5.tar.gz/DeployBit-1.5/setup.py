from distutils.core import setup
import textwrap

setup(
  name = 'DeployBit',
  packages = ['DeployBit'],
  version = '1.5',
  license='MIT',   
  description = 'A New Door to Salesforce',
    long_description=open('README.rst', 'r').read(),
    long_description_content_type='text/x-rst',
  author = 'Padmnabh Munde',
  author_email = 'padmnabhmunde77@gmail.com',
  keywords = ['Salesforce', 'DeployBit','DeployBit Python', 'Deploy','Deployment','Retrieve','Metadata API','SOAP API','Query','SOQL'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
  ],
)