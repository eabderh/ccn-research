#!/usr/bin/python


import subprocess
from subprocess import call

lrange = map(str, range(1,8))
hosts = list("h" + member for member in map(str, range(0,2)))
nodes = list("b" + member for member in map(str, range(0,1)))
targets = hosts + nodes

print targets

def exec_ssh_commands(targets, ssh_commands):
    for target in targets:
        for ssh_command in ssh_commands:
            command = "ssh {} \"{}\"".format(target, ssh_command)
            print command
            #call(command, shell=True)

def exec_remote_script(targets, script):
    for target in targets:
        command = "scp {} {}:.".format(script, target)
        print command
        #call(command, shell=True)
    ssh_commands = ["sudo chmod +x " + script, "./" + script]
    exec_ssh_commands(targets, ssh_commands)


exec_remote_script(targets, "test.sh")



