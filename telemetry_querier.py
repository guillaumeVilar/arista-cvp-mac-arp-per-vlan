from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec.custom_types import FrozenDict
from cloudvision.Connector.codec import Wildcard, Path
import tempfile
import ssl
import os
import json


os.environ["GRPC_VERBOSITY"] = "NONE"
mac_per_vlan_export_filename = "mac_per_vlan.json"
arp_per_interface_export_filename = "arp_per_interface.json"

class TelemetryQuerier:
    def __init__(self, cvp_ip, token):
        ssl._create_default_https_context = ssl._create_unverified_context
        ca_fd, ca_path = tempfile.mkstemp()
        with os.fdopen(ca_fd, "wb") as tmp:
            tmp.write(str.encode(ssl.get_server_certificate((cvp_ip, 443))))
        self.client = GRPCClient(
            f"{cvp_ip}:443",
            tokenValue=token,
            ca=ca_path
        )
        os.remove(ca_path)
        # Create an empty dict to store all the mac per vlan in format: 
        # {100: {'ca:fe:ca:fe:ca:fe'}, 200: {'00:1c:73:aa:bb:cc'}} 
        self.mac_in_vlan = {}
        # Create an empty dict to store all the Ip present in each vlan in format: 
        # {Vlan100: {'10.92.64.2'}, Vlan200: {'10.92.65.174'}} 
        # This info is based on the arp entry on the aggregate switches
        self.arp_entries_per_interface = {}

    def store_mac_in_each_vlan_for_device(self, device):
        pathElts = [ "Smash", "bridging", "status", "smashFdbStatus" ]
        query = [ create_query([(pathElts, [])], device) ]

        for batch in self.client.get(query):
            for notif in batch["notifications"]:
                updates = notif["updates"]

                for k, v in updates.items():
                    mac_add = v["key"]["addr"]
                    vlan = v["key"]["fid"]["value"]
                    if vlan not in self.mac_in_vlan.keys():
                        # Creating a set to store the mac for that vlan
                        self.mac_in_vlan[vlan] = set()

                    # As set only store unique value, there is no need to check uniqueness
                    self.mac_in_vlan[vlan].add(mac_add)
        return

    # Store each arp entry learned in a Vlan* interface inside a dict of set.
    def store_arp_entry_for_each_vlan_for_device(self, device):
        pathElts = [ "Smash", "arp", "status", "arpEntry" ]
        query = [ create_query([(pathElts, [])], device) ]

        for batch in self.client.get(query):
            for notif in batch["notifications"]:
                updates = notif["updates"]

                for k, v in updates.items():
                    # print(f"k: {k}")
                    # print(f"v: {v}")
                    addr = k["addr"]
                    intfId = k["intfId"]
                    # print(f"addr: {addr} - intf {intfId}")

                    if intfId not in self.arp_entries_per_interface.keys():
                        # Creating a set to store the arp entry for that interface
                        self.arp_entries_per_interface[intfId] = set()



                    # As set only store unique value, there is no need to check uniqueness
                    self.arp_entries_per_interface[intfId].add(addr)
        return


    def get_all_device_serial_number(self):
        list_devices_serial_number = []
        dataset = "cvp"
        pathElts = [ "inventory", "device", "ids" ]
        query = [create_query([(pathElts, [])], dataset)]
        for batch in self.client.get(query):
            for notif in batch["notifications"]:
                updates = notif["updates"]
                list_devices_serial_number.append(list(updates.keys())[0])
        return list_devices_serial_number
    

    # Export the data to a json file

    def export_result(self, dict_to_export, filename):
        print(f"===== Exporting data to {filename} =====")

        # Modify the set inside the dict as a list to be able to export the data to json
        json_serializable_dict = {dict_key: list(set_data) for dict_key, set_data in dict_to_export.items()}

        # Open the file in write mode and use json.dump() to write the dictionary to the file
        with open(filename, 'w') as json_file:
            json.dump(json_serializable_dict, json_file, indent=4)  # 'indent' is optional, for pretty-printing
        
        print(f"===== DONE Exporting data to {filename} =====")

    def export_all_to_json(self):
        if self.mac_in_vlan != {}:
            self.export_result(self.mac_in_vlan, mac_per_vlan_export_filename)
        if self.arp_entries_per_interface != {}:
            self.export_result(self.arp_entries_per_interface, arp_per_interface_export_filename)

    def print_number_of_mac_per_vlan(self):
        print(f"===== Number of mac per VLAN =====")
        for vlan, mac_list in self.mac_in_vlan.items():
            print(f"{vlan} - {len(mac_list)}")
        print(f"===== DONE Number of mac per VLAN =====")
    
    def print_number_of_arp_per_interface(self):
        print(f"===== Number of arp entry per interface =====")
        for interface, arp_entry_list in self.arp_entries_per_interface.items():
            print(f"{interface} - {len(arp_entry_list)}")
        print(f"===== DONE Number of arp entry per interface =====")
