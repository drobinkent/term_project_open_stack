import compute
import network
import infrastructure
import disk
import utilities


import jsonpickle
import pprint as pp
import json
import openstack


def get_conn():
    conn=openstack.connect(
            auth_url='https://openstack.tacc.chameleoncloud.org:5000/v2.0',
            project_name='CH-819892',
            username='drobin',
            password='cloud_KENT',
            region_name='RegionOne',
            app_name='examples',
            app_version='1.0',
        )
    print(conn)
    return conn

# infra = infrastructure.Infrastructure()
# com = compute.Compute()
# print(com)
# comlist = []
# comlist.append(com)
# com = compute.Compute()
# comlist.append(com)
# com = compute.Compute()
# comlist.append(com)

# for i in comlist:
#     infra.add_compute_node(i)

# com = network.Network()
# print(com)
# comlist = []
# comlist.append(com)
# com = network.Network()
# comlist.append(com)
# com = network.Network()
# comlist.append(com)

# for i in comlist:
#     infra.add_network(i)


# com = disk.Disk()
# print(com)
# comlist = []
# comlist.append(com)
# com =  disk.Disk()
# comlist.append(com)
# com =  disk.Disk()
# comlist.append(com)

# for i in comlist:
#     infra.add_Disk(i)
# serialized = jsonpickle.encode(infra)
# pp.pprint(serialized)
# x = pp.PrettyPrinter()
# #x.pprint(serialized)
# my_car_obj = jsonpickle.decode(serialized)
# print(my_car_obj)



# with open("/Users/debobrotodasrobin/Google Drive/kent univ/spring_2018/cloud_infra/term_project/gcp_libcloud_term_project/gcp_resources/cloud.config" , 'r') as f:
#     dat = f.read()
#     p = jsonpickle.decode(dat)
#     print("Data is ",p)
#     print("salkdfjskdfas\n\n\n")
#     print(jsonpickle.encode(p))

def test_infra():

    openstack_con = get_conn()
    # all_ips = openstack_con.network.ips()
    # openstack_con
    # print("Printing all ips")
    # for ip in all_ips:
    #     print(ip)
    # # print(utilities.list_flavors(openstack_con))
    # networks_list, networks_subnet_ids_list= utilities.list_networks(openstack_con)
    # for n in networks_list:
    #     print(n)
    # servers_list, servers_host_id_list, servers_name_list = utilities.list_servers(openstack_con)
    # for s in servers_list:
    #     print(s)
    #     print("Address of the servers are ")
    #     print(s.addresses)

    
    infra = infrastructure.Infrastructure("/Users/debobrotodasrobin/Google Drive/kent univ/spring_2018/cloud_infra/term_project_open_stack/openstack/gcp_resources/cloud.config")
    infra.stop_resources(openstack_con)
    infra.start_resources(openstack_con)
    #infra.stop_resources(openstack_con)
    #infra.deploy_task_script()

test_infra()