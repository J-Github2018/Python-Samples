i#!/usr/bin/env python


import csv
import paramiko
import time




serverlist = []
#This function ask for the file location of the csv file and then appends the rows to the Variables,
#please note that this function is designed to retrieve data from 1 columns.
def get_memory():
    file_path = './serverlist.csv'
    with open(file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV) # Skip the first 'title' row.
        for row in readCSV:
            columnA = serverlist.append(row[0])

            if row[0] != '': #this if conditional gets rid of '' from the list
                columnA
        print('Your lists of servers are {}'.format(serverlist))

    k = paramiko.RSAKey.from_private_key_file("/home/ec2-user/.ssh/2020.pem")
    c = paramiko.SSHClient()

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.load_system_host_keys()
    print "connecting"


    for server in serverlist:
        try:
            c.connect( hostname = server, username = "ec2-user", pkey = k, port=22 )
            print ("connected to ",server)
            commands = [ "hostname", "ps -o pid,user,%mem,command ax | sort -b -k3 -r" ]
            for command in commands:
                print "Executing {}".format( command )
                stdin , stdout, stderr = c.exec_command(command)
                print stdout.read()
        except Exception as e:
             print('ERROR: SSH conection too ' + server + ' Failed due to the following error =====>', e)
        finally:
            c.close()



get_memory()


