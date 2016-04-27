#!/usr/bin/python

import geni_interface as gi

#mesh = gi.geni()
#mesh.manifest_file = "manifest_mesh.xml"
#mesh.sshconfig_file = "ccnx_sshconfig.txt"
#mesh.log_formatname = "log_mesh/{target}_ifconfig-log.txt"
#mesh.init()

branch = gi.geni()
branch.manifest_file = "manifest_branch.xml"
branch.sshconfig_file = "ccnx_sshconfig.txt"
branch.log_formatname = "log_branch/{target}_{logfile}"
branch.testnode = "node1210"
branch.data_file = "data_branch"
branch.turns = range(0,4)
branch.run = "6"
branch.init()
#branch.nodes = ["node2210"]

