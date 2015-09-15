#!/usr/bin/env python

"""
Simple program that will take input from command line. The program will then create the .j2 and .yml files in the current working directory. 
Some error checking is installed. Basic network skills would be required to answer the inputs.

Deveployed by Trace3 during APO Partner Rotation 9-7-2015 thru 9-18-2015.
"""


from sys import version_info
import xmltodict
import json
import sys
import re

def yml_prep(file):
    # This preps the yml
    file.write("---\n")
    file.write("\n")

def exit(yml_file,j2_file):
    yml_file.close()
    j2_file.close()
    sys.exit(0)

def is_ipv4(ip):
    # Checks the formatting of the IP address using a regex expression 
    match = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip)
    if not match:
        return False
    return True

def is_ipv4_with_CIDR(ip):
    # Checks the formatting of the IP address and CIDR using a regex expression 
    match = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$", ip)
    if not match:
        return False
    return True

def get_hostname(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your hostname: ")
    while len(response) > 32:
        print "Hostname has to be less than 32 characters. Please try again."
        response = raw_input("Please enter your hostname: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("hostname: "+response+"\n\n")
    j2_file.write("\nhostname {{ hostname }}\n\n")

def get_username(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your username: ")
    while response.isdigit():
        print "Username cannot be all numbers. Please try again."
        response = raw_input("Please enter your username: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("username: "+response+"\n\n")
    j2_file.write("username {{ username }} ")

def get_password(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your password: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("password: "+'"'+response+'"'"\n\n")
    j2_file.write("password {{ password }}  role network-admin\n\n")

def get_motd(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your message of the day: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("banner_motd: "+'"'+response+'"'+"\n\n")
    j2_file.write("banner motd *\n    {{ banner_motd }}\n*\n\n")

def get_domain(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your domain-name: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("domian: "+response+"\n\n")
    j2_file.write("ip domain-name {{ domain }}\n\n")

def get_vtp(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your vtp mode: \n1: Server 2: Client 3: Transparent 4: Off ")
    if response == exit_code:
        exit(yml_file,j2_file)
    while response != "1" and response != "2" and response != "3" and response!= "4" and response!= exit_code:
        print "Entry is invalid. Please try again:\n"
        switchport = raw_input("Please enter your vtp mode: \n1: Server 2: Client 3: Transparent 4: Off ")
    if response == "1":
        yml_file.write("vtp_mode: Server \n\n")
    if response == "2":
        yml_file.write("vtp_mode: Client \n\n")
    if response == "3":
        yml_file.write("vtp_mode: Transparent \n\n")
    if response == "4":
        yml_file.write("vtp_mode: Off \n\n")
    if response == exit_code:
        exit(yml_file,j2_file)
    j2_file.write("vtp mode {{ vtp_mode }}\n\n")

def get_snmp(exit_code,yml_file,j2_file):
    response = raw_input("Please enter your snmp-server contact: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("snmp:\n  { contact: "+response+", ")
    j2_file.write("snmp-server contact {{ snmp.contact }}\n")

    response = raw_input("Please enter your snmp-server location: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("location: "+response+", ")
    j2_file.write("snmp-server location {{ snmp.location }}\n")

    response = raw_input("Please enter your snmp-server read only string: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("ro_string: "+response+", ")
    j2_file.write("snmp-server community {{ snmp.ro_string }} group network-operator\n")

    response = raw_input("Please enter your snmp-server read write string: ")
    if response == exit_code:
        exit(yml_file,j2_file)
    yml_file.write("rw_string: "+response+" }\n\n")
    j2_file.write("snmp-server community {{ snmp.rw_string }} group network-admin\n\n")
	
def get_ntp(exit_code,yml_file,j2_file):
    response = raw_input("Please enter the IP address of the NTP server (format - X.X.X.X): ")
    if response == exit_code:
        exit(yml_file,j2_file)
    test = is_ipv4(response)
    while test == False:
        response = raw_input("Please enter a proper IP address (format - X.X.X.X): ")
        test = is_ipv4(response)   
    else:
        yml_file.write("ntp_server: "+response+"\n\n")
        j2_file.write("ntp server {{ ntp_server }}\n\n")
		
def get_mgmt(exit_code,yml_file,j2_file):
    response = raw_input("Please enter the mgmt IP address (format - X.X.X.X/XX): ")
    if response == exit_code:
        exit(yml_file,j2_file)
    test = is_ipv4_with_CIDR(response)
    while test == False:
        response = raw_input("Please enter a proper IP address and CIDR (format - X.X.X.X/XX): ")
        test = is_ipv4_with_CIDR(response)   
    else:
        yml_file.write("mgmt_ip: "+response+"\n\n")
        j2_file.write("interface mgmt0"+"\n  "+"vrf member management"+"\n  "+"IP address {{ mgmt_ip }}\n\n")
        #####Default Gateway#####
        response = raw_input("What is the default gateway for the management IP (format - X.X.X.X): ")
        test = is_ipv4(response)
        while test == False:
            response = raw_input("Please enter a proper IP address (format - X.X.X.X): ")
            test = is_ipv4(response)   
        else:
            yml_file.write("""vrf_name: management"""+"\n"+"""route: "ip route 0.0.0.0/0 """+response+""""\n\n""")
            j2_file.write("vrf context {{ vrf_name }}"+"\n  "+"ip domain-name {{ domain }}"+"\n  "+"{{ route }}\n\n")	
			
def get_vlan(exit_code,yml_file,j2_file):
    response = raw_input("Would you like to configure VLANs. Plese enter (y) or (n): ")
    if response == exit_code:
        exit(yml_file,j2_file)
    while response != "y" and response != "n":
        response = raw_input("Please enter (y) or (n): ")
    if response == "n":
        exit
    if response == "y":
        yml_file.write("vlans:")
        j2_file.write("{% for vlan in vlans %}\nvlan {{ vlan.id }}\n{%- if vlan.name %}\n  name {{ vlan.name }}\n{%- endif %}\n{%- endfor %}\n\n")

        while response == "y":
            vlan_id = raw_input("Please enter the vlan ID: ")
            while any(not c.isdigit() for c in vlan_id):
               print "Vlan ID has to be a number. Please try again:"
               vlan_id = raw_input("Please enter the vlan ID: ")
            vlan_name = raw_input("Please enter the vlan name: ")
            yml_file.write("\n"+"  "+"- { id: "+vlan_id+", name: "+vlan_name+" }")
            response = raw_input("Would you like to configure another VLAN? Plese enter (y) or (n): ")
            while response != "y" and response != "n":
                response = raw_input("Please enter (y) or (n): ")
        else:
            yml_file.write("\n\n")		

def get_interface(exit_code,yml_file,j2_file):
    response = raw_input("Would you like to configure interface(s). Plese enter (y) or (n): ")
    if response == exit_code:
        exit(yml_file,j2_file)
    while response != "y" and response != "n":
        response = raw_input("Please enter (y) or (n): ")
    if response == "n":
        exit
    if response == "y":
        yml_file.write("interfaces:\n")
        j2_file.write("{%- for interface in interfaces %}\n")
        j2_file.write("interface {{ interface.intf }}\n")
        j2_file.write("  {{ interface.switchport }}\n")
        j2_file.write("{%- if interface.switchport == 'no switchport' %}\n")
        j2_file.write("  ip {{ interface.ip }}\n")
        j2_file.write("{%- endif %}\n")
        j2_file.write("{%- if interface.switchport == 'switchport' %}\n")
        j2_file.write("  switchport mode {{interface.mode}}\n")
        j2_file.write("{%- if interface.mode == 'access' %}\n")
        j2_file.write("  switchport access vlan {{ interface.access_vlan }}\n")
        j2_file.write("{%- endif %}\n")
        j2_file.write("{%- if interface.mode == 'trunk' %}\n")
        j2_file.write("  switchport trunk native vlan {{ interface.native_vlan }}\n")
        j2_file.write("  switchport trunk allowed vlan {{ interface.vlan_range }}\n")
        j2_file.write("{%- endif %}\n")
        j2_file.write("{%- endif %}\n")
        j2_file.write("{%- endfor %}\n\n")
        while response == "y":
            interface_id = raw_input("Please enter an interface you would like to configure. Please enter it in the format of example \n Ethernet 1/4. You would only enter 1/4: ")
            yml_file.write("  - { intf: Ethernet"+interface_id+", ")
            switchport = raw_input("Please enter 1: for switchport 2: for no switchport: ")
            while switchport != "1" and switchport != "2":
                print "Entry is invalid. Please try again:"
                switchport = raw_input("Please enter 1: for switchport 2: for no switchport: ")

            if switchport == "1":
                yml_file.write("switchport: switchport, ")
                mode = raw_input("Please enter mode for the interface 1: for access 2: for trunk: ")
                while mode != "1" and mode != "2":
                    print "Entry is invalid. Please try again:"
                    mode = raw_input("Please enter mode for the interface 1: for access 2: for trunk: ")

                if mode == "1":
                    yml_file.write("mode: access, ")
                    vlan_id = raw_input("Please enter please enter access VLAN ID: ")
                    while any(not c.isdigit() for c in vlan_id):
                        print "VLAN ID has to be a number. Please try again:"
                        vlan_id = raw_input("Please enter the VLAN ID: ")
                    yml_file.write("access_vlan: "+vlan_id+", ")
                else:
                    yml_file.write(" mode: trunk, ")
                    vlan_id = raw_input("Please enter please enter native VLAN ID: ")
                    # Work on check for vlan range
                    while any(not c.isdigit() for c in vlan_id):
                        print "VLAN ID has to be a number. Please try again:"
                        vlan_id = raw_input("Please enter the VLAN ID: ")
                    yml_file.write("native_vlan: "+vlan_id+", ")
                    vlan_range = raw_input("Please enter please enter trunk vlan range: ")
                    while any(c.isalpha() for c in vlan_range):
                        print "Trunk VLAN range has to be numbers. Please try again:"
                        vlan_range = raw_input("Please enter please enter trunk vlan range: ")
                    yml_file.write("vlan_range: "+'"'+vlan_range+'"'+", ")
            else:
                yml_file.write("switchport: "+'"'+"no switchport"+'"'+", ") 
                ip = raw_input("Please enter please enter an IP address with CIDR. Example 192.168.1.1/24: ")
                while not (is_ipv4_with_CIDR(ip)):
                    print "Please enter a proper IP address and CIDR (format - X.X.X.X/XX): "
                    ip = raw_input("Please enter please enter an IP address with CIDR. Example 192.168.1.1/24: ")
                yml_file.write("ip: "+ip+", ")
            #####SHUTDOWN#####
            shutdown = raw_input("Please enter 1: for shutdown 2: for no shutdown: ")
            while shutdown != "1" and shutdown != "2":
                print "Entry is invalid. Please try again:"
                shutdown = raw_input("Please enter 1: for shutdown 2: for no shutdown: ")
            if shutdown == "1":
                yml_file.write("state: shutdown"+" }\n")
            else:
                yml_file.write("state: "+'"'+"no shutdown"+'"'" }\n")
            response = raw_input("Would you like to configure another interface? Plese enter (y) or (n): ")
            while response != "y" and response != "n":
                response = raw_input("Please enter (y) or (n): ")
        else:
            yml_file.write("\n\n")


def main():
    exit_code = 'exit'
    response = 'test1'

    print "At anytime type "+exit_code+" as a response to a question and system will exit. All open files will be closed and saved as is"
    print "At this stage the program does not do error checking. That could be added later"

    response = raw_input("Please enter name of your project: ")
    if response == exit_code:
        sys.exit(0)
    print "All files will be named '"+response+"'"

    yml_file_name = response + '.yml'
    yml_file = open(yml_file_name, "w")
    j2_file_name = response + '.j2'
    j2_file = open(j2_file_name, "w")

    yml_prep(yml_file) 

    get_hostname(exit_code,yml_file,j2_file)
    get_username(exit_code,yml_file,j2_file)
    get_password(exit_code,yml_file,j2_file)
    get_motd(exit_code,yml_file,j2_file)
    get_domain(exit_code,yml_file,j2_file)
    get_vtp(exit_code,yml_file,j2_file)
    get_snmp(exit_code,yml_file,j2_file)
    get_ntp(exit_code,yml_file,j2_file)
    get_vlan(exit_code,yml_file,j2_file)
    get_interface(exit_code,yml_file,j2_file)
    get_mgmt(exit_code,yml_file,j2_file)
	
    exit(yml_file,j2_file)

if __name__ == "__main__":
    main()