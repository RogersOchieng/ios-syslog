import os.path
import sys
import getpass 
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
from datetime import datetime
from threading import Thread
import sys



startTime = datetime.now()
userName = input('Please enter your username: ')
passWord = getpass.getpass(prompt='Please enter your password: ') 
syslog_host = input('Please enter IP Address of your Syslog Server: ')
template="""logging host {}
gw-accounting syslog\n""".format(syslog_host)
generatedconfig=template
generatedconfig=generatedconfig.split("\n")
print (generatedconfig)
	
threads = []
def checkparallel(ip):
	device = ConnectHandler(device_type='cisco_ios', ip=ip, username=userName, password=passWord)
	device.send_config_set(generatedconfig)
	device.send_command("write memory")
	output = device.send_command("show run | in hostname")
	output=output.split(" ")
	hostname=output[1]
	#perform validations
	print ("************************************")
	print ("Performing validation for :",hostname+"\n")
	output=device.send_command("show logging")
	if ("encryption disabled, link up"):
		print ("Syslog is configured and reachable")
	else:
		print ("Syslog is NOT configured and NOT reachable")
#	if ("Trap logging: level informational" in output):
#		print ("Logging set for informational logs")
#	else:
#		print ("Logging not set for informational logs")

	print ("***********************************\n")


#Checking IP address file and content validity
def ip_file_valid():

    #Prompt user for input
    ip_file = input ("\n# Enter IP file pathe and name (e.g D:\ip.txt) ")
    
    #Checking if file exists
    if os.path.isfile(ip_file) == True:
        print("n\* IP file is valid :)\n")
        
    else:
        print("\n* File {} does not exist :( Please check and try again.\n".format(ip_file))
        sys.exit()
        
    #Open user selected file for reading (IP addresses file)
    selected_ip_file = open(ip_file, 'r')
    
    #Starting from the beginning of the file
    selected_ip_file.seek(0)
    
    #Reading each line (IP address) in the file
    ip_list = selected_ip_file.readlines()
    
    #Closing the file
    selected_ip_file.close()
    
    return ip_list


 		
ip_list = ip_file_valid()

try:
    
	for ip in ip_list:
		ip = ip.rstrip()
		t = Thread(target=checkparallel, args= (ip,))
		t.start()
		threads.append(t)

		#wait for all threads to completed
		for t in threads:
			t.join()
	
		print ("\nTotal execution time:")
		print(datetime.now() - startTime)
    
except NetMikoTimeoutException:
	print ("Host unreachable")
	
except NetMikoAuthenticationException:
	print ("Authentication Error")

#except Exception as e:
#	print ("An Error has occured")
	
