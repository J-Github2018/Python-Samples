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
    file_path = input('Please enter file CSV file location: ')
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
    key_path = input('Please enter the file location of the PEM file: ')
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
                    host = server.replace('.','_')
                    stdin , stdout, stderr = c.exec_command(f"echo Jarush_Epic_Games.Jarush.Amazon_EC2.{host}.UsedMemory {i} `date +%s` | nc 172.31.32.181 2003")
        except Exception as e:
             print('ERROR: For server: ' + server + ' failed due to the following error =====>', e)
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

