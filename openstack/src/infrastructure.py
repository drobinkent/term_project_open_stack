import network
import compute
import disk
import os
import jsonpickle
import sys
import traceback
import datetime
import time
import router



class Infrastructure :
    # def __init__ (self):
    #     self.networks = []
    #     self.compute_nodes = []
    #     self.Disks = []
    #     return
    
    def add_network(self, network):
        self.networks.append(network)

    def get_network_by_name(self, name):
        for net in self.networks:
            if net.name == name :
                return net
        return None
    
    def add_compute_node(self, compute_node):
        self.compute_nodes.append(compute_node)

    def add_Disk(self, Disk):
        self.Disks.append(Disk)

    def add_Router(self, router):
        self.routers.append(router)

    def get_router_by_name(self, name):
        for rtr in self.routers:
            if rtr.name == name :
                return rtr
        return None
    
    def __init__(self, file_path = None):
        self.networks = []
        self.compute_nodes = []
        self.Disks = []
        self.routers= []
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                try:
                    # do stuff
                    data = f.read()
                    p = jsonpickle.decode(data)
                    self.networks = p.networks
                    self.compute_nodes= p.compute_nodes
                    self.Disks = p.Disks
                    self.routers = p.routers
                    print("Data is ",p)
                    print(jsonpickle.encode(self.Disks ))
                except Exception:
                    print("Exception occured in infrastrcuture file parsing. Exiting",Exception,traceback.print_exc())  
                    sys.exit(1)
        else:
            print("Infrastrucutre config file not found. check the file path or name!!. Exiting")
            sys.exit(1)
           # handle error
        return


    def start_resources(self, driver):
        print("Starting all resources of infrastrucutre..... ")
        # for disk in self.Disks:
        #     disk.start_disk(driver)
        for net in self.networks:
            net.start_network(driver)
        for vm in self.compute_nodes:
            vm.start_compute_node(driver, self.get_network_by_name(vm.name))  
        for r in self.routers:
            r.create_router(driver)
            print ( "Router created")
        for net in self.networks:
            r = driver.network.find_router(net.router) #this is openstack router object. Not your router. remember
            i = driver.network.find_subnet(net.subnet.name).id
            if r and i : 
                rtr_inf= driver.network.add_interface_to_router(router = r, subnet_id=i, port_id=None)
                my_router = self.get_router_by_name(net.router)
                my_router.subnet_interface_list.append(net.subnet.name)                
                print(" Interface added :",rtr_inf)
        print("Started all resources of infrastrucutre..... ")
        return

    def stop_resources(self, driver):
        print("Stoping all resources of infrastrucutre..... ")
        # for disk in self.Disks:
        #     disk.stop_hdd(driver)
        
        for vm in self.compute_nodes:
            vm.stop_compute_node(driver)   
        for net in self.networks:
            net.stop_sub_networks(driver)
        for r in self.routers:
            r.stop_and_del_router(driver)
            print ( "Router Deleted")
        for net in self.networks:
            net.stop_network(driver)
        print("Stopped all resources of infrastrucutre..... ")
        return


    def display(self, title, resource_list=[]):
        """
        Display a list of resources.
        :param  title: String to be printed at the heading of the list.
        :type   title: ``str``
        :param  resource_list: List of resources to display
        :type   resource_list: Any ``object`` with a C{name} attribute
        """
        print('=> %s' % title)
        for item in resource_list:
            if hasattr(item, 'name'):
                print('     %s' % item.name)
            else:
                print('     %s' % item)

    def deploy_task_script(self):
        for node in self.compute_nodes:
            node.deploy_task_scipt()
        for node in self.compute_nodes:
            node.ssh_thread.thread.join()
