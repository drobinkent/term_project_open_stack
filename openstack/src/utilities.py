
import compute
import network
import infrastructure
import disk
import utilities
import openstack
import pprint


import jsonpickle
import pprint as pp
import json
import os
import errno





def show_instance_options(driver):
    images = list(driver.image.images())
    for image in images :
        print(image)
    locations = driver.list_locations()
    pprint.pprint(locations)
    sizes = driver.sizes()
    pprint.pprint(sizes)
    return




def list_images(conn):
    pprint.pprint("List Images:")
    images_list=[]
    images_id_list=[]
    images_name_list=[]
    try:
        for image in conn.image.images():
            images_list.append(image)
            images_id_list.append(image.id)
            images_name_list.append((image.id, image.name))
    except Exception as ex:
        pprint.pprint("Caught exception in listing images",ex)
    return images_list,images_id_list, images_name_list



def list_networks(conn):
    print("List Networks:")
    networks_list=[]
    networks_subnet_ids_list=[]
    try :
        for network in conn.network.networks():
            networks_list.append(network)
            networks_subnet_ids_list.append(network.subnet_ids)
    except Exception as ex:
        print("Caught exception in listing networks",ex)
    return networks_list, networks_subnet_ids_list

def list_flavors(conn):
    flavor_list = conn.compute.flavors()
    flavor_name_list=[]    

    for f in flavor_list:
        flavor_name_list.append(f.name)
    return flavor_list,flavor_name_list


def list_servers(conn):
    servers_list=[]
    servers_host_id_list=[]
    servers_name_list=[]    
    try:
        for server in conn.compute.servers():
            servers_list.append(server)
            servers_host_id_list.append(server.host_id)
            servers_name_list.append((server.host_id, server.instance_name))
    except Exception as ex:
        print("Caught exception in listing servers",ex)
    return servers_list, servers_host_id_list, servers_name_list

def delete_all_resources(conn):
    servers_list, servers_host_id_list, servers_name_list = list_servers(conn)
    for s in servers_list:
        conn.delete_server(s.name)
    routers = conn.network.routers()
    networks_list, networks_subnet_ids_list = list_networks(conn)
    for n in networks_list:
        subnets = conn.network.subnets()
        for s in subnets:
            conn.network.delete_subnet(s)
    print("Deleted all subnets")
    for r in routers:
        conn.network.delete_router(r, ignore_missing=True)
    for n in networks_list:
        conn.network.delete_network(n, ignore_missing=False)
    print(networks_list)







def create_server(conn,SERVER_NAME, IMAGE_NAME, FLAVOR_NAME, NETWORK_NAME, USER_ID,ADMIN_PASSWORD ):
    pprint.pprint("Create Server:")

    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    #keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,user_id =USER_ID,admin_password=ADMIN_PASSWORD,
        networks=[{"uuid": network.id}], #key_name=keypair.name
        )

    server = conn.compute.wait_for_server(server)

    # print("ssh -i {key} root@{ip}".format(
    #     key=global_config.PRIVATE_KEYPAIR_FILE,
    #     ip=server.access_ipv4))
    return server




def find_network( conn, name):
    print("Find Network:",name)
    network = conn.network.find_network(name_or_id=name)
    print(network)
    return network