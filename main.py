"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from ncclient import manager
from ncclient.operations.rpc import RPC
from lxml import etree
import time


class SendCommand(RPC):
    """
    Create a new class that inherit from ncclient.operations.rpc.RPC
    """

    # Override request method
    def request(self, xml):
        # Send request
        return self._request(xml)


if __name__ == "__main__":
    # Change the following with your credentials
    # NetConf server username
    USER = ""  # change username
    # NetConf server IP
    HOST = ""  # change host ip
    # NetConf server ssh port
    PORT = 830
    # NetConf server password
    PASSWORD = ""  # change password

    xml = """<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <target>
      <candidate/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration>
            <active>act</active>
            <interface-name>Loopback1</interface-name>
            <interface-virtual/>
            <description>NetConfDescriptionDemo123</description>
            <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
                <addresses>
                    <primary>
                        <address>172.16.0.1</address>
                        <netmask>255.255.255.255</netmask>
                    </primary>
                </addresses>
            </ipv4-network>
            <shutdown/>
        </interface-configuration>
      </interface-configurations>
     </config>
    </edit-config>
    """

    # Connect to NetConf server
    m = manager.connect(host=HOST, port=PORT, username=USER, password=PASSWORD, hostkey_verify=False, device_params={},
                        look_for_keys=False, allow_agent=False)

    # Create a new SendCommand instance class defined above
    rpc_call = SendCommand(m._session,
                           device_handler=m._device_handler,
                           timeout=m._timeout,
                           raise_mode=m._raise_mode)

    # Do the request and save the response into a variable
    response = rpc_call.request(xml=etree.fromstring(xml))

    print(response)

    # Commit changes
    xml = '<commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>'
    response = rpc_call.request(xml=etree.fromstring(xml))

    # Print response
    print(response)

    # Wait for router to process the request before closing the connection
    time.sleep(5)
