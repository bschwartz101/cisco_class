#!/usr/bin/env python

from sys import version_info
import sys
import re

"""
Simple program that will take input from command line. Then create a file with html and Body data need to run in Postman. 
Some error checking is installed. Basic network skills would be required to answer the inputs.

Deveployed by Trace3 during APO Partner Rotation 9-7-2015 thru 9-18-2015.
"""

def exit(file):
    file.close()
    sys.exit(0)

def is_ipv4_with_CIDR(ip):
    # Checks the formatting of the IP address and CIDR using a regex expression 
    match = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$", ip)
    if not match:
        return False
    return True

def get_ACI_Login(file):
    data = []
    aci_hostname = raw_input("Please enter the ACI Hostname: ")
    while " " in aci_hostname:
        print "ACI Hostname not cointain a space. Please try again:"
        aci_hostname = raw_input("Please enter the ACI Hostname: ")
    aci_username = raw_input("Please enter the ACI Username: ")
    while " " in aci_username:
        print "ACI Username not cointain a space. Please try again:"
        aci_username = raw_input("Please enter the ACI Username: ")
    aci_password = raw_input("Please enter the ACI Password: ")
    while " " in aci_password:
        print "ACI Password not cointain a space. Please try again:"
        aci_password = raw_input("Please enter the ACI Password: ")
    data.append(aci_hostname)
    data.append(aci_username)
    data.append(aci_password)
    file.write("*******ACI Login*****\n")
    file.write("URL:\n")
    file.write("https://"+aci_hostname+"/api/aaaLogin.xml\n")
    file.write("Data:\n")
    file.write("<aaaUser name=" + "'" + aci_username + "'" + " pwd=" + "'" + aci_password + "'" + "/>\n\n")
    #get_tenant(file,aci_hostname)
    return data

def get_tenant(file,data):
    tenant_name = raw_input("Please enter the Tenant Name: ")
    while " " in tenant_name:
        print "Tenant Name not cointain a space. Please try again:"
        tenant_name = raw_input("Please enter the Tenant Name: ")
    data.append(tenant_name)
    aci_hostname = data[0]
    file.write("*******Tenant: "+ tenant_name + "*****\n")
    file.write("URL:\n")
    file.write("https://" + aci_hostname +"/api/node/mo/uni/tn-"+ tenant_name +".json\n")
    file.write("Body:\n")
    file.write("{"+'"'+"fvTenant"+'"'+":{"+'"'+"attributes"+'"'+":{"+'"'+"dn"+'"'+":"+'"'+"uni/tn-"+ tenant_name+""+'"'+","+'"'+"name"+'"')
    file.write(":"+'"'+""+ tenant_name+""+'"'+","+'"'+"rn"+'"'+":"+'"'+"tn-"+ tenant_name+""+'"'+","+'"'+"status"+'"'+":"+'"'+"created"+'"'+"},"+'"'+"children"+'"'+":[]}}\n\n")
    return data

def get_vrf(file,data):
    aci_hostname = data[0]
    tenant_name = data[3]
    VRF_name = raw_input("Please enter the new VRF Name: ")
    while " " in VRF_name:
        print "VRF Name not cointain a space. Please try again:"
        VRF_name = raw_input("Please enter the new VRF Name: ")
    data.append(VRF_name)
    file.write("*******Tenant: "+ tenant_name + " VRF: " +VRF_name+ "*****\n")
    file.write("URL:\n")
    file.write("https://"+ aci_hostname +"/api/node/mo/uni/tn-"+ tenant_name +"/ctx-"+ VRF_name +".json\n")
    file.write("Body\n")
    file.write("{"+ '"' +"fvCtx"+ '"' +":{"+ '"' +"attributes"+ '"' +":{"+ '"' +"dn"+ '"' +":"+ '"' +"uni/tn-"+ tenant_name +"/ctx-"+ VRF_name +""+ '"' +","+ '"' +"name"+ '"')
    file.write(":"+ '"' +""+ VRF_name +""+ '"' +","+ '"' +"rn"+ '"' +":"+ '"' +"ctx-"+ VRF_name +""+ '"' +","+ '"' +"status"+ '"' +":"+ '"' +"created"+ '"' +"},"+ '"' +"children"+ '"' +":[]}}\n\n")
    return data

def get_BD(file,data):
    aci_hostname = data[0]
    tenant_name = data[3]
    VRF_name = data[4]
    bd_name = raw_input("Please enter a new Bridge Domian Name: ")
    while " " in bd_name:
        print "Bridge DomianName not cointain a space. Please try again:"
        bd_name = raw_input("Please enter a new Bridge Domian Name: ")
    data.append(bd_name)
    another_ip = 'y'
    while another_ip  == 'y': 
        response = raw_input("Please enter a new bridge domain subnet IP address and CIDR (format - X.X.X.X/XX): ")
        test = is_ipv4_with_CIDR(response)
        while test == False:
            response = raw_input("Please enter a proper IP address and CIDR (format - X.X.X.X/XX): ")
            test = is_ipv4_with_CIDR(response)
        bd_IP = response   
        response = raw_input("Please enter a new bridge domain subnet scope \n1: Shared\n2: Public\n3: Private\n: ")
        while response != "1" and response != "2" and response != "3":
            print "Entry is invalid. Please try again:\n"
            response = raw_input("Please enter a new bridge domain subnet scope \n1: Shared\n2: Public\n3: Private\n: ")
        if response == "1":
            bd_Scope = "shared"
        if response == "2":
            bd_Scope = "public"
        if response == "3":
            bd_Scope = "private"

        file.write("*******Tenant: "+ tenant_name + " VRF: " +VRF_name+ " Bridge Domain: "+bd_name+ " Subnet: "+ bd_IP +"*****\n")
        file.write("URL:\n")
        file.write("https://"+ aci_hostname +"/api/node/mo/uni/tn-"+ tenant_name + "/BD-" + bd_name + ".json\n")
        file.write("Body:\n")
        file.write("{"+ '"' +"fvBD"+ '"' +":{"+ '"' +"attributes"+ '"' +":{"+ '"' +"dn"+ '"' +":"+ '"' +"uni/tn-"+ tenant_name +"/BD-"+ bd_name +""+ '"' +","+ '"' +"name"+ '"' +":"+ '"' +""+ bd_name)
        file.write(""+ '"' +","+ '"' +"rn"+ '"' +":"+ '"' +"BD-"+ bd_name +""+ '"' +","+ '"' +"status"+ '"' +":"+ '"' +"created"+ '"' +"},"+ '"' +"children"+ '"' +":[{"+ '"' +"fvSubnet"+ '"') 
        file.write(":{"+ '"' +"attributes"+ '"' +":{"+ '"' +"dn"+ '"' +":"+ '"' +"uni/tn-"+ tenant_name +"/BD-"+ bd_name +"/subnet-["+ bd_IP +"]"+ '"' +","+ '"' +"ip"+ '"' +":"+ '"' +""+ bd_IP +""+ '"')
        file.write(","+ '"' +"scope"+ '"' +":"+ '"' +""+ bd_Scope +""+ '"' +","+ '"' +"rn"+ '"' +":"+ '"' +"subnet-["+ bd_IP +"]"+ '"' +","+ '"' +"status"+ '"' +":"+ '"' +"created"+ '"' +"},"+ '"')
        file.write("children"+ '"' +":[]}},{"+ '"' +"fvRsCtx"+ '"' +":{"+ '"' +"attributes"+ '"' +":{"+ '"' +"tnFvCtxName"+ '"' +":"+ '"' + VRF_name + '"' +","+ '"' +"status"+ '"' +":"+ '"') 
        file.write("created,modified"+ '"' +"},"+ '"' +"children"+ '"' +":[]}}]}}\n\n")

        another_ip = raw_input("Would you like to add another subnet to the "+ bd_name +" Bridge Domain? Plese enter (y) or (n): ")
        while another_ip!= "y" and another_ip != "n":
            another_ip = raw_input("Please enter (y) or (n): ")
    return data


def main():

    data = []
    another_tenant = 'y'
    another_bd = 'y'


    response = raw_input("Please enter the name of file the for output\n .txt will be appened to the end of file name: ")
    while " " in response:
        print "File name not cointain a space. Please try again:"
        response = raw_input("Please enter the name of file the for output\n .txt will be appened to the end of file name: ")
    file_name = response + ".txt"
    file = open(file_name, "w")

    data = get_ACI_Login(file)
    while another_tenant == "y":
        another_bd = 'y'
        data = get_tenant(file,data)
        tenant_name = data[3]
        data = get_vrf(file,data)
# Create a while to loop Bridge Domains
        while another_bd == "y":
            data = get_BD(file,data)
            another_bd = raw_input("Would you like to create another Bridge Domains in Tenant "+ tenant_name +"? Plese enter (y) or (n): ")
            while another_bd!= "y" and another_bd != "n":
                another_bd = raw_input("Please enter (y) or (n): ")
        another_tenant = raw_input("Would you like to create another Tenant? Plese enter (y) or (n): ")
        while another_tenant!= "y" and another_tenant != "n":
            another_tenant = raw_input("Please enter (y) or (n): ")
    #print data
    exit(file)

if __name__ == "__main__":
    main()
