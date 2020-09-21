'''Problem1
>Never had the chance to design a script like this, looking forward to the challege and learning as I go.
>Needed to figure what python module existed to help with this
>Started googleing for ideas
>I found a couple of possible solutions so I then started to narrow down to the least complicated solution

>Needed to figure out the approach I was going to take to get the memory usage per process for multiple servers
>Decided to have my python script be feed a csv file and it will parse the file for the servenames

>I setup an AWS account and spun up 2 EC2 to simulated running a machine on 1 machine that will retrieve information from both itself and the other cluser member

>I setup ssh access on both machines so that both python can run commands remotely on the other machine via ssh

> Took me about 4hrs to reliaze that this python script will fail if it tries to ssh to the itself via Ipaddress, will add some error handling to the script

>Reliase the script fails if the remote server does not already have the public key added to its known host file/ authorize key file. Need to figure out a way to automate that process.

> Added error handling but also with more troubleshooting I was able to get around the previous error by using the pem file generated by AWS instead of the id.rsa private key,
this also allows me to ssh to server without having to manually ssh to them first. Sweet!

>Will add in the input variable to ask for the file location of the pem.

> Created first working version of the script down and dirty now I need to refactor and modify it per client requirements, part of the requirements was to have this script run in "parrell"
makes me think that the script needs to run with multi-threading...will do some discovery on how to accomplish this.


> After a couple hours doing discovery on multi-threading vs multi-processing and trying to figure out to get that setup via python I finally got it figured out and get the script setup

> After countless hours of troubleshooting trying to figure out how to send the remote command to the servers and grap that output to send to Graphite I finally have a working POC that im proud of.
>Visit this URL (https://18.221.231.190/S/C) to see live data right now, I have the python script in cron to run every minute from my the bastion host of my AWS env.
'''
#!/usr/bin/env python3

import os
import csv
import pprint
import paramiko
from time import time
from threading import Thread



serverlist = []



#This function ask for the file location of the csv file and then appends the ro                                                                                        ws to the Variables,
#please note that this function is designed to retrieve data from 1 columns.
def get_serverlist():
    file_path = raw_input('Please enter file CSV file location: ')
    #file_path = './serverlist.csv'
    with open(file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV) # Skip the first 'title' row.
        for row in readCSV:
            columnA = serverlist.append(row[0])

            if row[0] != '': #this if conditional gets rid of '' from the list
                columnA
        print('Your lists of servers are {}'.format(serverlist))
        return serverlist




def get_memory():


    get_serverlist()
    ts = time()
    key_path = raw_input('Please enter the file location of the PEM file: ')
    #key_path='/home/ec2-user/.ssh/2020.pem'
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    commands = [ " ps -o %mem ax | grep -v %MEM" ]
    

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.load_system_host_keys()
    print ("connecting")


    for server in serverlist:
        try:
            c.connect( hostname = server, username = "ec2-user", pkey = k, port=22 )
            print ("connected to ",server)

            for command in commands:                
                stdin , stdout, stderr = c.exec_command(command)                
                for i in stdout.readlines():
                    i = float(i)
                    stdin , stdout, stderr = c.exec_command(f"echo Jarush_Epic_Games.Jarush.Amazon_EC2.UsedMemory {i} `date +%s` | nc 172.31.32.181 2003")
        #except Exception as e:
             #print('ERROR: For server: ' + server + ' failed due to the following error =====>', e)
        finally:
            c.close()
    print('Time took in secounds was', time() - ts)


threads =[]

for i in range(os.cpu_count()):
    print('registering thread {}'.format(i))
    threads.append(Thread(target=get_memory))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

