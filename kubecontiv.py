#!/usr/bin/python

'''
Created on 2016. 9. 8.

@author: "comfact"
'''

from pygics import *

#===============================================================================
# User Options
#===============================================================================
DEBUG = False
TRYCOUNT = 3
DELAY = 2

#===============================================================================
# Static Vars
#===============================================================================
COMMANDS = ['create', 'delete']

POD_TEMPLATE = '''
apiVersion: v1
kind: Pod
metadata:
  name: %s
  labels:
    app: %s
    io.contiv.tenant: %s
    io.contiv.net-group: %s
    io.contiv.network: %s
spec:
  containers:
  - name: %s
    image: %s
    command:
'''

POD_TEMPLATE_CMD = '      - %s\n'

#===============================================================================
# Functions
#===============================================================================
def usages():
    print 'kubecontiv.py <command> <description>'
    print '\t<command> : create, delete'
    exit()

def execute(cmd, cond=None, weak=False, infi=False):
    print 'execute >', cmd
    if DEBUG: return
    if cond != None:
        clause = cond[0]
        oper = cond[1]
        value = cond[2]
        print 'condition >', value, oper, clause
        ret, out = Command(clause).do()
        if oper == 'in':
            for o in out:
                if re.search('%s\s+' % value, o): break
            else:
                print '%s is not exist' % value
                return
        elif open == 'nin':
            for o in out:
                if re.search('%s\s+' % value, o):
                    print '%s is already exist' % value
                    return
    
    print 'do >',
    if infi == False:
        for i in range(0, TRYCOUNT):
            ret, out = Command(cmd).do()
            if ret == 0: print 'ok'; break
            print '\nerror! (%d)' % i
            print ''.join(out)
            time.sleep(DELAY)
        else:
            if weak == False: exit(1)
    else:
        while True:
            ret, out = Command(cmd).do()
            if ret == 0: print 'ok'; break
            print '\nerror! (%d)' % i
            print ''.join(out)
            time.sleep(DELAY)
    time.sleep(DELAY)
    
def write_file(path, data):
    print 'file >', path
    print data
    if DEBUG: return
    with open(path, 'w') as fd:
        fd.write(data)
        fd.flush()
    time.sleep(DELAY)

#===============================================================================
# Commands
#===============================================================================
def create(desc):
    
    for tenant in desc.tenant:
        
        print 'CREATE TENANT >', tenant.name
        execute('netctl tenant create %s' % tenant.name,
                ('netctl tenant ls', 'nin', tenant.name))
        
        for pol in tenant.policy:
            print 'PARSE POLICY >', pol.name
            
            for rule in pol.rule:
                print 'PARSE RULE >', 
                rule_options = ''
                try:
                    if 'priority' in rule: rule_options += '--priority %s ' % rule.priority
                    if rule.direction == 'in':
                        rule_options += '--direction in '
                        if 'from_network' in rule: rule_options += '--from-network %s ' % rule.from_network
                        if 'from_group' in rule: rule_options += '--from-group %s ' % rule.from_group
                        if 'from_ip' in rule: rule_options += '--from-ip-address %s ' % rule.from_ip
                    elif rule.direction == 'out':
                        rule_options += '--direction out '
                        if 'to_network' in rule: rule_options += '--to-network %s ' % rule.to_network
                        if 'to_group' in rule: rule_options += '--to-group %s ' % rule.to_group
                        if 'to_ip' in rule: rule_options += '--to-ip-address %s ' % rule.to_ip
                    else: continue
                    if 'protocol' in rule: rule_options += '--protocol %s ' % rule.protocol
                    if 'port' in rule: rule_options += '--port %s ' % rule.port
                    rule_options += '--action %s' % rule.action
                except Exception as e:
                    print 'ERROR >', str(e)
                    continue
                print 'OK'
                rule['options'] = rule_options
            
            print 'CREATE POLICY >', pol.name
            execute('netctl policy create -t %s %s' % (tenant.name, pol.name),
                    ('netctl policy ls -t %s', 'nin', pol.name))
        
        for prof in tenant.profile:
            prof['group_names'] = L()
            for net in prof.net:
                print 'CREATE NETWORK >', net.name
                execute('netctl network create -t %s --nw-type %s --encap %s --pkt-tag %s --subnet %s --gateway %s %s' % (tenant.name, net.type, net.encap, net.tag, net.subnet, net.gateway, net.name),
                        ('netctl network ls -t %s' % tenant.name, 'nin', net.name))
                
            for group in prof.group:
                prof.group_names << group.name
                pol_script = ''
                for pol_name in group.policy: pol_script += '--policy %s ' % pol_name
                
                print 'CREATE GROUP >', group.name
                execute('netctl group create -t %s %s%s %s' % (tenant.name, pol_script, group.net, group.name),
                        ('netctl group ls -t %s' % tenant.name, 'nin', group.name))
            
        for pol in tenant.policy:
            cnt = 1
            for rule in pol.rule:
                if 'options' in rule: 
                    print 'APPLY RULE >', rule.options
                    execute('netctl rule-add -t %s %s %s %d' % (tenant.name, rule.options, pol.name, cnt))
                    cnt += 1
        
        for prof in tenant.profile:
            print 'CREATE AND DEPLOY PROFILE >', prof.name
            execute('netctl app-profile create -t %s --group %s %s' % (tenant.name, ','.join(prof.group_names), prof.name),
                    ('netctl app-profile ls -t %s' % tenant.name, 'nin', prof.name))
            
        for prof in tenant.profile:
            for group in prof.group:
                for pod in group.pod:
                    print 'CREATE AND DEPLOY POD >', pod.name
                    pod_name = tenant.name + '-' + prof.name + '-' + group.name + '-' + pod.name
                    podexec = POD_TEMPLATE % (pod_name,
                                              prof.name,
                                              tenant.name,
                                              group.name,
                                              group.net,
                                              pod.cname,
                                              pod.image)
                    
                    for cmd in pod.command: podexec += POD_TEMPLATE_CMD % cmd
                    
                    Command('mkdir -p %s' % desc.project).do()
                    file_name = '%s/%s.yaml' % (desc.project, pod_name)
                    write_file(file_name, podexec)
                    execute('kubectl create -f %s' % file_name)
                    
def delete(desc):
    
    for tenant in desc.tenant:
        for prof in tenant.profile:
            for group in prof.group:
                for pod in group.pod:
                    print 'DELETE POD >', pod.name
                    pod_name = tenant.name + '-' + prof.name + '-' + group.name + '-' + pod.name
                    file_name = '%s/%s.yaml' % (desc.project, pod_name)
                    execute('kubectl delete -f %s' % file_name, weak=True)
                    Command('rm -rf %s' % file_name).do()
                    
        for prof in tenant.profile:
            print 'DELETE PROFILE >', prof.name
            execute('netctl app-profile delete -t %s %s' % (tenant.name, prof.name),
                    ('netctl app-profile ls -t %s' % tenant.name, 'in', prof.name),
                    weak=True)
            
            for group in prof.group:
                print 'DELETE GROUP >', group.name
                execute('netctl group delete -t %s %s' % (tenant.name, group.name),
                        ('netctl group ls -t %s' % tenant.name, 'in', group.name),
                        weak=True)
            
            for net in prof.net:
                print 'DELETE NETWORK >', net.name
                execute('netctl network delete -t %s %s' % (tenant.name, net.name),
                        ('netctl network ls -t %s' % tenant.name, 'in', net.name),
                        infi=True)
                
        for pol in tenant.policy:
            print 'DELETE POLICY >', pol.name
            execute('netctl policy delete -t %s %s' % (tenant.name, pol.name),
                    ('netctl policy ls -t %s' % tenant.name, 'in', pol.name),
                    weak=True)
        
        print 'DELETE TENANT >', tenant.name
        execute('netctl tenant delete %s' % tenant.name,
                ('netctl tenant ls', 'in', tenant.name),
                weak=True)

if __name__ == '__main__':
    alen = len(sys.argv)
    if alen < 3: usages()
    command = sys.argv[1]
    file = sys.argv[2]
    if alen >= 4 and sys.argv[3] == 'debug': DEBUG = True
    if command not in COMMANDS: usages()
    if not os.path.exists(file): usages()
    
    desc = M()
    with open(file, 'r') as fd:
        desc = Struct.JSON2DATA(''.join(fd.readlines()))
    desc['project'] = file.replace('.json', '')

    print "Description"    
    print inf(desc)
    print ""
    
    if command == 'create': create(desc)
    elif command == 'delete': delete(desc)
