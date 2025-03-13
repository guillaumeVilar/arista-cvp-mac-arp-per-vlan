# arista-cvp-mac-arp-per-vlan
> **Warning**
> Disclaimer: This project is not an officially endorsed or supported Arista project, and should be treated as a best-effort initiative, without any guarantee of performance or reliability.


A script to query mac and ARP information from telemetry data stored in Arista CVP platform, in order to count the number of unique mac and ARP entry per VLAN.


# Installation: 
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Then, modify the main.py to include a service-account token, and point to the CVP server. 
```
# From main.py:

# Replace the token value by a service account token (in CVP > General Settings > Service Accounts)
token = ""

# Replace this IP with the IP address of the primary CVP server
cvp_ip_address = "10.0.0.1"

```


# Usage:
```
python3 main.py
```

# Example of output: 
```
$ python3 main.py 
['<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>', '<S/N>']
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
Checking device <S/N>
===== Number of mac per VLAN =====
1006 - 4
100 - 1
200 - 1
1007 - 3
1008 - 3
1009 - 3
1010 - 3
1011 - 3
1012 - 3
1013 - 1
1015 - 1
1016 - 1
1017 - 1
1018 - 1
1019 - 1
1020 - 1
1021 - 1
1022 - 1
1024 - 1
1026 - 1
1028 - 1
1029 - 1
1030 - 1
1031 - 1
1032 - 1
1033 - 1
1034 - 1
1035 - 1
1036 - 1
1037 - 1
1039 - 1
1041 - 1
1042 - 1
1043 - 1
1044 - 1
1045 - 1
1046 - 1
1049 - 1
1050 - 1
1051 - 1
1052 - 1
1053 - 1
1054 - 1
1055 - 1
1056 - 1
1057 - 1
1058 - 1
1059 - 1
1060 - 1
1063 - 1
1064 - 1
1065 - 1
1067 - 1
1068 - 1
1070 - 1
1071 - 1
1072 - 1
1073 - 1
1074 - 1
1075 - 1
1076 - 1
1077 - 1
2000 - 1
1 - 2
50 - 6
4001 - 110
4093 - 4
4094 - 4
4005 - 1
10 - 3
20 - 4
===== DONE Number of mac per VLAN =====
===== Number of arp entry per vlan =====
Vlan4094 - 2
Vlan4093 - 2
Vlan50 - 4
===== DONE Number of arp entry per vlan =====
===== Exporting data to mac_per_vlan.json =====
===== DONE Exporting data to mac_per_vlan.json =====
===== Exporting data to arp_per_vlan.json =====
===== DONE Exporting data to arp_per_vlan.json =====
```