from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv


log = core.getLogger()
policyFile = "%s/Documents/Redes/miot/sdn/allowed_hosts" % os.environ[ 'HOME' ]

# Create a list of src/dst MAC Addr pairs to be allowed
allowList=list()

with open(policyFile) as f:
    for row in f:
        allowList.append(row[1:])

# Delete the first row since it is just header, not data
allowList.pop(0)


class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        for sublist in allowList:
            # Create a allow match
            allowRule = of.ofp_match()
            allowRule.dl_src = EthAddr(sublist[0])
            allowRule.dl_dst = EthAddr(sublist[1])
            
            # Create a message containing allowRule and send to OpenFlow Switch
            fm = of.ofp_flow_mod()
            fm.match = allowRule
            event.connection.send(fm)
            
            
    

    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
Starting the Firewall module
'''
    core.registerNew(Firewall)