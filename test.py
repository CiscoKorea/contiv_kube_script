#!/usr/bin/python

'''
Created on 2016. 9. 8.

@author: "comfact"
'''

from pygics import *

if __name__ == '__main__':
    
    cmd = Command('netctl')
    
    ret, out = cmd.add('tenant').add('ls').add('|').add('grep').add('default').do()
    
    print ret, out