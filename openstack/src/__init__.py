from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import pickle as pickle


ComputeEngine = get_driver(Provider.GCE)
# Note that the 'PEM file' argument can either be the JSON format or
# the P12 format.
driver = ComputeEngine("deba-385@booming-client-196602.iam.gserviceaccount.com", 
                    "/Users/debobrotodasrobin/Downloads/My Project 82646-993cc2e26380.json",
                       project="booming-client-196602")
nodes = driver.list_nodes()
for x in nodes :
    print(x)
    driver(x.name)

images = driver.list_images()
for i in images:
    if "ubuntu" in i.name: 
        #print(i)
        print(str(pickle.dumps(i)))
       

# sizes = driver.list_sizes()
# for s in sizes:
#     print(s)

# zones = driver.ex_list_zones()
# for  z in zones :
#     print(z)
