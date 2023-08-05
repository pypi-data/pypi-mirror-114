from .masternode_list_provider import MasternodeListProvider
import random

class MasternodeDiscovery:
    def __init__(self, seeds = None, port = None):
        self.mnlist_provider = MasternodeListProvider(seeds, port)
        self.seeds = seeds


    def get_random_masternode(self, excluded_ips = None):
        mnlist = self.mnlist_provider.get_mn_list()

        # Filter out excluded mns
        #if (Array.isArray(excludedIps)):
        #  MNList = MNList.filter(mn => excludedIps.indexOf(mn.service.split(':')[0]) < 0);

        return random.sample(mnlist, 1)[0]['service']


    def get_mnlist(self):
        return self.mnlist_provider.get_mn_list()


    def check_mn_response(self, ip_address):
        return self.mnlist_provider.check_mn_response(ip_address)


    def reset(self):
        self.mnlist_provider = MasternodeListProvider(self.seeds);
