import xml.etree.ElementTree as ET
import re

xml_data = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><sessionId xmlns="">d22f8a39fab16973481b6a4074bcdb92</sessionId><command echo="" xsi:type="ServiceProviderGetListResponse" xmlns=""><serviceProviderTable><colHeading>Service Provider Id</colHeading><colHeading>Service Provider Name</colHeading><colHeading>Is Enterprise</colHeading><colHeading>Reseller Id</colHeading><row><col>wagerTest</col><col>test28</col><col>false</col><col/></row><row><col>Test</col><col/><col>false</col><col/></row><row><col>RPM_Enterprise_Demo_PHL10</col><col/><col>false</col><col/></row><row><col>3100001877</col><col/><col>true</col><col/></row><row><col>BSFTPHL10cluster</col><col/><col>true</col><col/></row><row><col>3100001897</col><col/><col>true</col><col/></row><row><col>Momentum_Retail_PHL10</col><col/><col>false</col><col/></row><row><col>3100002121</col><col/><col>true</col><col/></row><row><col>3100002214</col><col/><col>true</col><col/></row><row><col>3100002333</col><col/><col>true</col><col/></row><row><col>3100002643</col><col/><col>true</col><col/></row><row><col>3100002679</col><col/><col>true</col><col/></row><row><col>3100002820</col><col/><col>true</col><col/></row><row><col>3100002840</col><col/><col>true</col><col/></row><row><col>3100003038</col><col/><col>true</col><col/></row><row><col>3100003074</col><col/><col>true</col><col/></row><row><col>3100003138</col><col/><col>true</col><col/></row><row><col>3100003191</col><col/><col>true</col><col/></row><row><col>3100003213</col><col/><col>true</col><col/></row><row><col>3100003215</col><col/><col>true</col><col/></row><row><col>3100003216</col><col/><col>true</col><col/></row><row><col>3100003236</col><col/><col>true</col><col/></row><row><col>3100003244</col><col/><col>true</col><col/></row><row><col>3100003247</col><col/><col>true</col><col/></row><row><col>3100003611</col><col/><col>true</col><col/></row><row><col>byopstn</col><col/><col>true</col><col/></row><row><col>3100004690</col><col>WebExTestEntName</col><col>true</col><col/></row><row><col>3100004867</col><col/><col>true</col><col/></row><row><col>3100004872</col><col/><col>true</col><col/></row><row><col>3100004890</col><col/><col>true</col><col/></row><row><col>3100004901</col><col/><col>true</col><col/></row><row><col>3100004902</col><col/><col>true</col><col/></row><row><col>3100004916</col><col/><col>true</col><col/></row><row><col>3100004917</col><col/><col>true</col><col/></row><row><col>3100004944</col><col/><col>true</col><col/></row><row><col>3100004998</col><col/><col>true</col><col/></row><row><col>dummywebex</col><col/><col>true</col><col/></row><row><col>dummytest2</col><col/><col>true</col><col/></row><row><col>3100005051</col><col/><col>true</col><col/></row><row><col>3100005052</col><col/><col>true</col><col/></row><row><col>3100005053</col><col/><col>true</col><col/></row><row><col>3100005054</col><col/><col>true</col><col/></row><row><col>3100005060</col><col/><col>true</col><col/></row><row><col>3100005372</col><col/><col>true</col><col/></row><row><col>3100005574</col><col/><col>true</col><col/></row><row><col>3100005630</col><col/><col>true</col><col/></row><row><col>3100005633</col><col/><col>true</col><col/></row><row><col>3100005793</col><col/><col>true</col><col/></row><row><col>3100005814</col><col/><col>true</col><col/></row><row><col>3100005864</col><col/><col>true</col><col/></row><row><col>3100005963</col><col/><col>true</col><col/></row><row><col>DO_NOT_TOUCH_RPX_BSFTPHL10</col><col/><col>false</col><col/></row><row><col>coreytest</col><col/><col>true</col><col/></row></serviceProviderTable></command></BroadsoftDocument>'''

# Remove namespaces
xml_data = re.sub(' xmlns="[^"]+"', '', xml_data, count=1)

# Parse the XML
root = ET.fromstring(xml_data)

# Find the serviceProviderTable element
table = root.find('.//serviceProviderTable')

# List to store 'Service Provider Id' values
service_provider_ids = []

# Check if table is found
if table is not None:
    # Extract column headings
    col_headings = [col.text for col in table.findall('colHeading')]

    # Walk through each row in the table
    for row in table.findall('row'):
        cols = [col.text if col.text is not None else "" for col in row.findall('col')]
        # Create a dictionary for each row
        row_data = dict(zip(col_headings, cols))
        # Add 'Service Provider Id' to the list
        service_provider_ids.append(row_data.get('Service Provider Id', ''))

print(service_provider_ids)