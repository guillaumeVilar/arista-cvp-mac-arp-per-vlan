from telemetry_querier import TelemetryQuerier

# Replace the token value by a service account token (in CVP > General Settings > Service Accounts)
token = ""
# Replace this IP with the IP address of the primary CVP server
cvp_ip_address = "10.0.0.1"

querier = TelemetryQuerier(cvp_ip_address, token)


device_sn_list = querier.get_all_device_serial_number()
print(device_sn_list)
for device in device_sn_list:
    print(f"Checking device {device}")
    querier.store_mac_in_each_vlan_for_device(device)
    querier.store_arp_entry_for_each_vlan_for_device(device)


querier.print_number_of_mac_per_vlan()
querier.print_number_of_arp_per_vlan()
querier.export_all_to_json()
