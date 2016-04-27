#!/usr/bin/python

import geni_lib as gl
from geni_lib import *
import subprocess
from subprocess import call
import time
import re

class geni:
    def init(self):
        self.root = gl.parse_xmlfile(self.manifest_file)
        self.sshinfo = gl.parse_xmltree_ssh(self.root)
        self.targets = gl.sshinfo_allhosts(self.sshinfo)
        self.nodes = list(self.targets)
        self.nodes.remove(self.testnode)
    def makesshconfig(self):
        self.sshconfig_string = gl.sshconfig_sprint(self.sshinfo)
        gl.sshconfig_fprint(self.sshinfo, self.sshconfig_file)
    def testssh(self):
        gl.ssh_test_connection(self.targets)
    def getinfo(self):
        command = "scp {target}:route-log.txt " + self.log_folder
        gl.exec_command(self.targets, command)
        command = "scp {target}:ifconfig-log.txt " + self.log_folder
        gl.exec_command(self.targets, command)
    def install(self):
        command = "scp installccnx.sh {target}:."
        gl.exec_command(self.targets, command)
        commands = ["sudo chmod +x installccnx.sh"]
        gl.exec_ssh_commands(self.targets, commands)
        command = "sudo ./installccnx.sh 2>&1 > log"
        #command = "sleep 4; echo \"test\""
        gl.exec_ssh_command_parallel(self.targets, command)
    def buildconfig(self):
        self.routeinfo = gl.parse_log(self.targets, self.log_formatname)
        gl.buildcfg(self.targets, self.routeinfo)
    def runmetis(self):
        self.metis_options = "--log all=debug"
        metis_path = "CCNx_Distillery/usr/bin/"
        metis_command = "sudo " + metis_path + \
            "metis_daemon --config \~/metis.cfg " + \
            self.metis_options
        for target in self.targets:
            ssh_command = "ssh {target} \"\"" + metis_command + "\"\""
            ssh_command = ssh_command.format(target=target)
            command = "tmux new-window \"{ssh_command};\""
            command = command.format(ssh_command=ssh_command)
            print command
            call(command, shell=True)
    def endmetis(self):
        command = "pgrep metis_daemon | sudo xargs kill"
        gl.exec_ssh_command_parallel(self.targets, command)
    def filet(self):
        command = "scp file.txt {target}:{target}.txt"
        gl.exec_command(self.targets, command)
        commands = ["sudo mkdir ~/servFiles", "sudo mv ~/node*.txt ~/servFiles"]
        gl.exec_ssh_commands(self.targets, commands)
        commands = ["sudo mkdir ~/servFiles", "sudo mv ~/centernode.txt ~/servFiles"]
        gl.exec_ssh_commands([self.targets[0]], commands)
    def test(self):
#        nodes = nodes[0:2]
        nodes = self.nodes
        testnode = self.testnode

        metis_path = "CCNx_Distillery/usr/bin/"

        ssh_command = "sudo " + metis_path + \
            "ccnxSimpleFileTransfer_Server -l lci:/ ~/servFiles"
        processes = []
        for node in nodes:
            command = "ssh {} \"{}\"".format(node, ssh_command)
            print command
            p = Popen(command, shell=True)
            processes.append(p)

        for turn in self.turns:
            command = "mkdir turn" + str(turn)
            print command
            call(command, shell=True)
            for node in nodes:
                ssh_commands = ["sudo " + metis_path + \
                    "ccnxSimpleFileTransfer_Client -l lci:/ fetch " + \
                    node + ".txt > log_" + node]
                print ssh_commands
                gl.exec_ssh_commands([testnode], ssh_commands)
                command = "scp {target}:log_" + node + " turn" + str(turn) + "/."
                print command
                gl.exec_command([testnode], command)
            raw_input()
            command = "mv turn" + str(turn) + "/ run" + self.run + "/"
            print command
            call(command, shell=True)

        time.sleep(2)
        for p in processes:
            while p.poll() is None:
                gl.exec_ssh_command_parallel(nodes, "pgrep Simple | sudo xargs kill")

    def parsedata(self):
        nodes = self.nodes
        testnode = self.testnode
        data = []
        for turn in self.turns:
            data_turn = []
            for node in nodes:
                with open("run" + self.run + "/turn" + str(turn) + "/log_" + node) as f:
                    string = f.read().split("\n")
                lastline = string[-2]
                rate = re.findall("\d+\.\d+",lastline)
                rate = float(rate[0])
                print node
                print rate
                data_turn.append(rate)
            avg = reduce(lambda x, y: x + y, data_turn) / len(data_turn)
            data_turn.append(avg)
            data.append(data_turn)
        print data
        self.data = data
        with open(self.data_file + "_run" + self.run + ".txt", "w" ) as f:
            for turn in self.turns:
                l = "\n".join([str(x) for x in data[turn]])
                f.write(l + "\n\n")






