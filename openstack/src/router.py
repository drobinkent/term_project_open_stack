import GLOBAL_CONFIG as global_config


class Router:
    def __init__ (self,name = None):
        self.name = name
        self.subnet_interface_list = []
        return None
    
    def create_router(self,conn):
        print("create router         : %s" %self.name)
        self.subnet_interface_list = []
        external_network = conn.network.find_network(global_config.EXTERNAL_NETWORK_NAME)
        self.router =  conn.network.create_router(name=self.name,
                                      external_gateway_info={"network_id": external_network.id})
        return self.router

    

    def add_interface(self,conn, subnet_id_for_interface ):
        #self.router = conn.network.add_interface_to_router(router = self.router, subnet_id=subnet_id_for_interface, port_id=None)
        self.subnet_interface_list.append(subnet_id_for_interface)
        return self.router

    def remove_interface(self,conn, subnet_id_for_interface =None):
        self.router = conn.network.remove_interface_from_router(self.router, subnet_id=subnet_id_for_interface, port_id=None)
        return self.router

        
    def stop_and_del_router(self, conn):
        r = conn.network.find_router(self.name)
        print("Deleting Router")
        try :
            for snet_name in self.subnet_interface_list:
                id = conn.network.find_subnet(snet_name).id
                self.router = conn.network.remove_interface_from_router(r, subnet_id=id, port_id=None)
        except:
            print("Exception in removng interface from router")
        r = conn.network.find_router(self.name)
        if r is not None :
            conn.network.delete_router(r, ignore_missing=True)
        print(" Router Deleted")
        return

    
