import utilities
import GLOBAL_CONFIG as global_config
import time
class Network:
    
    def __init__ (self, name = None , cidr = None, mode = 'auto', router = "None" ):
        self.name = name 
        self.cidr = cidr
        self.mode = mode
        self.router = router
        return
    
    def start_network(self, conn) :
        print("Creating Network:")
        example_network = conn.network.create_network(
            name=self.name)
        print(example_network)
        print("Creating Sub Network:")
        example_subnet = conn.network.create_subnet(
            name="subnet-of-"+self.name,
            network_id=example_network.id,
            dns_nameservers=[global_config.GOOGLE_DNS_SERVER_IP],
            ip_version='4',
            cidr=self.cidr,
            is_dhcp_enabled = True)
        print(example_subnet)
        
        self.subnet = example_subnet
        return example_network

    def stop_sub_networks(self, conn) :
        print("Deleting  sub Networks:")
        network_to_be_deleted = utilities.find_network(conn, self.name)
        rtr = conn.network.find_router(self.router)
        
        try:
            for example_subnet in network_to_be_deleted.subnet_ids:
                conn.network.remove_interface_from_router(rtr, example_subnet)
                time.sleep(5)
                conn.network.delete_subnet(example_subnet, ignore_missing=False)
        except AttributeError:
            print("Exception in deleting network", AttributeError)

    def stop_network(self, conn) :
        print("Delete Network:")
        network_to_be_deleted = utilities.find_network(conn, self.name)
        try:
            for example_subnet in network_to_be_deleted.subnet_ids:
                conn.network.delete_subnet(example_subnet, ignore_missing=False)
        except AttributeError:
            print("Exception in deleting network", AttributeError)
        
        if network_to_be_deleted is not None:
            conn.network.delete_network(network_to_be_deleted, ignore_missing=False)
        return None

  

   
    