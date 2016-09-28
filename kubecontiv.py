#!/usr/bin/python

'''
Created on 2016. 9. 8.

@author: "comfact"
'''

from pygics import *

COMMANDS = ['create', 'delete']
DEBUG = True
#DEBUG = False

CONTTPL = '''apiVersion: v1
kind: Pod
metadata:
  name: %s-%s
  labels:
    app: %s
    io.contiv.tenant: %s
    io.contiv.net-group: %s
    io.contiv.network: %s-bd1
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

def condexec(cmd, clause, condition):
    if DEBUG: print 'EXECUTE >', clause; print 'EXECUTE >', cmd; return

    print 'EXECUTE >', clause
    ret, out = Command(clause).do()
    for o in out:
        if re.search('%s\s+' % condition, o): break
    else:
        print 'EXECUTE >', cmd
        ret, out = Command(cmd).do()
        if ret != 0: print 'ERROR! :', clause; exit(1)
        else: print ''.join(out)
        time.sleep(1)
    
def mustexec(cmd):
    if DEBUG: print 'EXECUTE >', cmd; return
    
    print 'EXECUTE >', cmd
    ret, out = Command(cmd).do()
    if ret != 0: print 'ERROR! :', cmd; exit(1)
    else: print ''.join(out)
    time.sleep(1)
        
def writefile(path, data):
    if DEBUG: print 'FILE >', path; print data; return
    
    print 'FILE >', path
    print data
    with open(path, 'w') as fd:
        fd.write(data)
        fd.flush()
    time.sleep(1)

def create(desc):
    
    for tenant in desc.tenant:
        condexec('netctl tenant create %s' % tenant.name,
                 'netctl tenant ls | grep %s' % tenant.name,
                 tenant.name)
        
        app_names = L()
        for app in tenant.app:
            app_names << app.name
            
            group_names = L()
            for group in app.group:
                group_names << group.name
                
                net_name = group.name + '-bd1'
                
                condexec('netctl network create -t %s -n %s -e %s -p %s -s %s -g %s %s' % (tenant.name, group.type, group.encap, group.tag, group.subnet, group.gateway, net_name),
                         'netctl network ls -t %s | grep %s' % (tenant.name, net_name),
                         net_name)
                
                condexec('netctl group create -t %s %s %s' % (tenant.name, net_name, group.name),
                         'netctl group ls -t %s | grep %s' % (tenant.name, group.name),
                         group.name)
            
            condexec('netctl app-profile create -t %s -g %s %s' % (tenant.name, ','.join(group_names), app.name),
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
                    
                    writefile(file_name, podexec)
                    mustexec('kubectl create -f %s' % file_name)
                    
def delete(desc):
    
    for tenant in desc.tenant:
        
        for app in tenant.app:
            
            for group in app.group:
                
                for pod in group.pod:
                    
                    file_name = tenant.name + '-' + pod.name + '.yaml'
                    
                    mustexec('kubectl delete -f %s' % file_name)
                    mustexec('rm -rf %s' % file_name)
        
    for tenant in desc.tenant:
        
        for app in tenant.app:
            
            mustexec('netctl app-profile delete -t %s %s' % (tenant.name, app.name))
            
            for group in app.group:
                
                mustexec('netctl group delete -t %s %s' % (tenant.name, group.name))
                mustexec('netctl network delete -t %s %s' % (tenant.name, group.name + '-bd1'))
            
        mustexec('netctl tenant delete %s' % tenant.name)

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
