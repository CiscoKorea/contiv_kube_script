#!/usr/bin/python

'''
Created on 2016. 9. 8.

@author: "comfact"
'''

import os
import sys
import json
from pygics import *

COMMANDS = ['create', 'delete']

def usages():
    print 'kubecontiv.py <command> <description>'
    print '\t<command> : create, delete'
    exit()
    
def create(desc):
    
    pass

def delete(desc):
    
    pass    

if __name__ == '__main__':

    print "Hello"
    
    if len(sys.argv) != 3: usages()
    command = sys.argv[1]
    file = sys.argv[2]
    if command not in COMMANDS: usages()
    if not os.path.exists(file): usages()
    
    desc = M()
    with open(file, 'r') as fd:
        desc = Struct.JSON2DATA(''.join(fd.readlines())) 

    print "Description"    
    print inf(desc)
    print ""
    
    if command == 'create': create(desc)
    elif command == 'delete': delete(desc) 
    
    
# "TENANT=test
# 
# # Network #########################################################
# NETWORK=test-net
# NET_TYPE=data
# NET_ENC=vlan
# NET_TAG=112
# NET_SUB=10.1.1.0/24
# NET_GW=10.1.1.1
# 
# # Group ###########################################################
# GROUP=test-epg
# 
# # App Profile #####################################################
# APPPROF=test-app
# 
# # Pod #############################################################
# PODNAME=test" 
# 
# echo "Create Tenant"
# echo "RUN : netctl tenant create $TENANT"
# netctl tenant create $TENANT
# sleep 1
# 
# echo "RUN : netctl network create -t $TENANT -n $NET_TYPE -e $NET_ENC -p $NET_TAG -s $NET_SUB -g $NET_GW $NETWORK"
# netctl network create -t $TENANT -n $NET_TYPE -e $NET_ENC -p $NET_TAG -s $NET_SUB -g $NET_GW $NETWORK
# sleep 1
# 
# echo "RUN : netctl group create -t $TENANT $NETWORK $GROUP"
# netctl group create -t $TENANT $NETWORK $GROUP
# sleep 1
# 
# echo "RUN : netctl app-profile create -t $TENANT -g $GROUP $APPPROF"
# netctl app-profile create -t $TENANT -g $GROUP $APPPROF
# sleep 1
# 
# 
# 
# metadata:
#   name: $TENANT-$PODNAME
#   labels:
#     app: $APPPROF
#     io.contiv.tenant: $TENANT
#     io.contiv.net-group: $GROUP
#     io.contiv.network: $NETWORK
# spec:
#   containers:
#   - name: bbox
#     image: contiv/nc-busybox
#     command:
#       - sleep
#       - "7200"
#     
