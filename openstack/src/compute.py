
from infrastructure import Infrastructure as infra
import GLOBAL_CONFIG as global_config
import os
import errno
import utilities
import paramiko_ssh


class Compute:
    
    def deploy_task_scipt(self):
        with open(self.task_script, "r") as ins:
            command_array = []
            for line in ins:
                command_array.append(line)
        self.ssh_thread = paramiko_ssh.ssh(self.ip,self.USER_ID,self.ADMIN_PASSWORD,command_array)
        return None

    def __init__ (self, name = None , instance_type = None, image= None , startup_script = None ,
        network_name = None, size = None,ADMIN_PASSWORD = global_config.ADMIN_PASSWORD,
        mem_size = None, num_cpus = None,USER_ID = global_config.USER_ID, task_script=None,ip = None):
        self.name = name 
        self.instance_type = instance_type
        self.image = image
        self.startup_script = startup_script
        self.metadata = {}
        self.network_name = network_name
        self.size = size
        self.location = "us-east4-a"
        self.mem_size =  mem_size
        self.num_cpus = num_cpus
        self.USER_ID = USER_ID
        self.ADMIN_PASSWORD = ADMIN_PASSWORD
        self.ip = ip
        self.server = None
        self.floating_ip_address = None
        self.task_script = task_script
        return
    
    '''
    In this function 
    Have to check if all the parameters are perfectly setup or not
    '''
    def start_compute_node(self, driver, network = None) :
        self.USER_ID = global_config.USER_ID
        self.ADMIN_PASSWORD = global_config.ADMIN_PASSWORD
        new_server = self.create_server(driver, self.name, self.image,
            self.instance_type,self.network_name, self.USER_ID,self.ADMIN_PASSWORD)
        #print("Creating a server interface")
        # serv_interface = driver.compute.create_server_interface(new_server, )
        # print(serv_interface)
        self.server= new_server
        return self.server

    def stop_compute_node(self,conn):
        server_to_be_delted = conn.compute.find_server(self.name)
        try:
            if (self.floating_ip_address is not None)  and (server_to_be_delted is not  None):
                conn.compute.remove_floating_ip_from_server(server_to_be_delted, self.floating_ip_address)
                conn.network.delete_ip(self.floating_ip_address, ignore_missing=True)     
        except:
            print("Eception in removng floating ip address")
        if(server_to_be_delted is not  None):
            conn.delete_server(self.name)
        return None

    def create_keypair(self,conn ):
        keypair = conn.compute.find_keypair(global_config.KEYPAIR_NAME)
        if not keypair:
            print("Create Key Pair:")
            keypair = conn.compute.create_keypair(name=global_config.KEYPAIR_NAME)
            print(keypair)
            try:
                os.mkdir(global_config.SSH_DIR)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e
            with open(global_config.PRIVATE_KEYPAIR_FILE, 'w') as f:
                f.write("%s" % keypair.private_key)
            os.chmod(global_config.PRIVATE_KEYPAIR_FILE, 0o400)
        return keypair

    def create_server(self, conn,SERVER_NAME, IMAGE_NAME, FLAVOR_NAME, NETWORK_NAME, USER_ID,ADMIN_PASSWORD ):
        print("Create Server:")

        image = conn.compute.find_image(IMAGE_NAME)
        flavor = conn.compute.find_flavor(FLAVOR_NAME)
        network = utilities.find_network(conn, NETWORK_NAME)
        keypair = self.create_keypair(conn)

        server = conn.compute.create_server(
            name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,user_id =USER_ID,admin_password=ADMIN_PASSWORD,
            networks=[{"uuid": network.id}], key_name=keypair.name
            )

        server = conn.compute.wait_for_server(server)
        self.server = server
        print("ssh -i {key} root@{ip}".format(
            key=global_config.PRIVATE_KEYPAIR_FILE,
            ip=server.access_ipv4))
        f_ip = conn.network.find_available_ip()
        print("All addresses of the server are")
        print(self.server.addresses[self.network_name])
        self.floating_ip_address = f_ip.floating_ip_address
        floating_network = utilities.find_network(conn, global_config.EXTERNAL_NETWORK_NAME)
        
        print("Got a floating ip to attch :", f_ip)
        if self.floating_ip_address is not None:
            conn.compute.add_floating_ip_to_server(self.server, self.floating_ip_address, fixed_address=self.server.addresses[self.network_name][0]['addr'])
        
        return server


    
