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
DEBUG = False

CONTTPL = '''metadata:
  name: %s-%s
  labels:
    app: %s
    io.contiv.tenant: %s
    io.contiv.net-group: %s
    io.contiv.network: %s-bd
spec:
  containers:
  - name: %s
    image: %s
    command:
'''

CONTCMD = '      - %s\n'

def usages():
    print 'kubecontiv.py <command> <description>'
    print '\t<command> : create, delete'
    exit()

def do(cmd, clause, name):
    if DEBUG:
        print cmd
    else:
        _, out = Command(clause).do()
        if name not in out:
            _, out = Command(cmd).do()
            
def execute(cmd):
    if DEBUG:
        print cmd
    else:
        _, out = Command(cmd).do()
            
def write(path, data):
    if DEBUG:
        print 'FILE :', path
        print data
    else:
        with open(path, 'w') as fd:
            fd.write(data)
            fd.flush()

def create(desc):
    
    for tenant in desc.tenant:
        do('netctl tenant create %s' % tenant.name,
           'netctl tenant ls | grep %s' % tenant.name,
           tenant.name)
        
        app_names = L()
        for app in tenant.app:
            app_names << app.name
            
            group_names = L()
            for group in app.group:
                group_names << group.name
                
                net_name = group.name + '-bd'
                
                do('netctl network create -t %s -n %s -e %s -p %s -s %s -g %s %s' % (tenant.name, group.type, group.encap, group.tag, group.subnet, group.gateway, net_name),
                   'netctl network ls -t %s | grep %s' % (tenant.name, net_name),
                   net_name)
                
                do('netctl group create -t %s %s %s' % (tenant.name, net_name, group.name),
                   'netctl group ls -t %s | grep %s' % (tenant.name, group.name),
                   group.name)
            
            do('netctl app-profile create -t %s -g %s %s' % (tenant.name, ','.join(group_names), app.name),
               'netctl app-profile ls -t %s | grep %s' % (tenant.name, app.name),
               app.name)
            
    for tenant in desc.tenant:
        
        for app in tenant.app:
            
            for group in app.group:
                
                for pod in group.pod:
                    
                    podexec = CONTTPL % (tenant.name,
                                         pod.name,
                                         app.name,
                                         tenant.name,
                                         group.name,
                                         group.name,
                                         pod.cname,
                                         pod.image)
                    
                    for cmd in pod.command:
                        podexec += CONTCMD % cmd
                    
                    file_name = tenant.name + '-' + pod.name + '.yaml'
                    
                    write(file_name, podexec)
                    execute('kubectl create -f %s' % file_name)

def delete(desc):
    
    pass    

if __name__ == '__main__':
    
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

#     
