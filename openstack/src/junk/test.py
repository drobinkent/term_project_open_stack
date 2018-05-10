import toscaparser.tosca_template as t
from pprint import pprint
import yaml
import pickle
import compute
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


def init_tosca_template(tosca_file_path):
    tpl = t.ToscaTemplate(path = tosca_file_path)
    topo = tpl.topology_template
    all_nodes = topo.nodetemplates
    for n in all_nodes:
        if "tosca.nodes.Compute" in str(n.type):
            print( "Compute node--", n.name)
            manage_compute_node(n)
        elif "tosca.nodes.network.Network" in str(n.type):
            print( "Network node--", n.name)
            manage_network(n)
        else:
            print("Unknown node -- ", n.name)
    return

def manage_compute_node(tosca_node):
    caps = tosca_node._capabilities
    server = compute.Compute ()
    server.name = tosca_node.name

    for cap in caps:
        print("Capability name : -- ", cap.name)
        if "host" in cap.name :
            print("host properties are")
            print("\t disk size of compute node is : ", cap._properties.get('disk_size'))
            server.size =  cap._properties.get('disk_size')
            print("\t Memory of compute node is : ", cap._properties.get('mem_size'))
            server.mem_size =  cap._properties.get('mem_size')
            print("\t num_cpus of compute node is : ", cap._properties.get('num_cpus'))
            server.num_cpus =  cap._properties.get('num_cpus')

        elif  "os" in cap.name :
            print("os properties are")
            print("\t Instance type of compute node is : ", cap._properties.get('type'))
            server.instance_type =  cap._properties.get('type')
            print("\t Num of CPU in compute node is : ", cap._properties.get('distribution'))
            server.image =  cap._properties.get('distribution')
    ComputeEngine = get_driver(Provider.GCE)
    # Note that the 'PEM file' argument can either be the JSON format or
    # the P12 format.
    driver = ComputeEngine("deba-385@booming-client-196602.iam.gserviceaccount.com", 
                        "/Users/debobrotodasrobin/Downloads/My Project 82646-993cc2e26380.json",
                        project="booming-client-196602")
    newly_created_node = server.create(driver)
    print(newly_created_node)
    return

def manage_network(tosca_net):
    props = tosca_net._properties
    for prop in props:
        print("Properties name : -- ", prop.name)
        if "ip_version" in prop.name :
            print("ip_version", prop.value)
        elif  "cidr" in prop.name :
            print("cidr", prop.value)
        elif  "start_ip" in prop.name :
            print("start_ip", prop.value)
        elif  "end_ip" in prop.name :
            print("end_ip", prop.value)
        elif  "gateway_ip" in prop.name :
            print("gateway_ip", prop.value)
        elif  "dhcp_enabled" in prop.name :
            print("dhcp_enabled", prop.value)
        else:
            print("Unknonwn proerty in network")
    return

# tpl = t.ToscaTemplate(path = "/Users/debobrotodasrobin/Google Drive/kent univ/spring_2018/cloud_infra/term_project/gcp_libcloud_term_project/gcp_resources/tosca_def.yaml")

# print(tpl.version)
# print(tpl.description)
# topo = tpl.topology_template
# all_nodes = topo.nodetemplates
# for x in all_nodes:
#     pprint(x.type)
#     caps = x._capabilities
#     print("x._capabilities's type is ",type(x._capabilities))
#     print("x._capabilitie[0]s's type is ",type(x._capabilities[0]))
#     print("x._capabilitie[0]s's name is ",x._capabilities[0].name)
#     print("x._capabilities[0]._propertiess type is ",type(x._capabilities[0]._properties))
#     for y in caps:
#         print("\t", y._properties)
#     print("architecture  name is :", caps[0]._properties.get("architecture"))
#     props = x._properties
#     print("x._properties's type is ",type(x._properties))
#     print("x._properties[0]s's type is ",type(x._properties[0]))
#     print("x._properties[0]s's name is ",x._properties[0].name)
#     for y in props:
#         print("\t", y)
    

# print(tpl.verify_template())


init_tosca_template("/Users/debobrotodasrobin/Google Drive/kent univ/spring_2018/cloud_infra/term_project/gcp_libcloud_term_project/gcp_resources/tosca_def.yaml")