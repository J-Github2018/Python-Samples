Problem 1 (My Thought Process)

Never had the chance to design a script like this, looking forward to the challege and learning as I go.

Needed to figure what python module existed to help with this

Started googleing for ideas

I found a couple of possible solutions so I then started to narrow down to the least complicated solution

Needed to figure out the approach I was going to take to get the memory usage per process for multiple servers

Decided to have my python script be feed a csv file and it will parse the file for the servenames

I setup an AWS account and spun up about 8-10 EC2's to simulated A bastion host that will SSH to other nodes to query and send the information to the Graphite server

I setup ssh access on both machines so that both python can run commands remotely on the other machine via ssh

Took me about 4hrs to reliaze that this python script will fail if it tries to ssh to the itself via Ipaddress, will add some error handling to the script

Reliase the script fails if the remote server does not already have the public key added to its known host file/ authorize key file. Need to figure out a way to automate that process.

Added error handling but also with more troubleshooting I was able to get around the previous error by using the pem file generated by AWS instead of the id.rsa private key,this also allows me to ssh to server without having to manually ssh to them first. Sweet!

Will add in the input variable to ask for the file location of the pem.

Created first working version of the script down and dirty now I need to refactor and modify it per client requirements, part of the requirements was to have this script run in "parrell" makes me think that the script needs to run with multi-threading...will do some discovery on how to accomplish this.

After a couple hours doing discovery on multi-threading vs multi-processing and trying to figure out to get that setup via python I finally got it figured out and get the script setup

After countless hours of troubleshooting trying to figure out how to send the remote command to the servers and grap that output to send to Graphite I finally have a working POC that im proud of.

Visit this URL (https://18.221.231.190/S/E) to see live data right now, I have the python script in cron to run every minute from my the bastion host of my AWS env.

