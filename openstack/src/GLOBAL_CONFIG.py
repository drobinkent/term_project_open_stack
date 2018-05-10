
import argparse
import os
import openstack
from openstack.config import loader
from openstack import utils
import sys



config = loader.OpenStackConfig()
cloud = conn=openstack.connect(
            auth_url='https://openstack.tacc.chameleoncloud.org:5000/v2.0',
            project_name='CH-819892',
            username='user',
            password='pass',
            region_name='RegionOne',
            app_name='examples',
            app_version='1.0',
        )



def _get_resource_value(resource_key, default):
    return config.get_extra_config('example').get(resource_key, default)

SERVER_NAME = 'openstacksdk-example'
IMAGE_NAME = _get_resource_value('image_name', 'cirros-0.3.5-x86_64-disk')
FLAVOR_NAME = _get_resource_value('flavor_name', 'm1.small')
NETWORK_NAME = _get_resource_value('network_name', 'private')


USER_ID   = "test"
ADMIN_PASSWORD ="test123"
KEYPAIR_NAME = _get_resource_value('keypair_name', 'cloud')
SSH_DIR = "/Users/debobrotodasrobin/.ssh/"
SSH_KEY_NAME = "cloud.pem"
SSH_KEY_PATH = SSH_DIR+SSH_KEY_NAME
PRIVATE_KEYPAIR_FILE = _get_resource_value(
    'private_keypair_file', '{ssh_dir}/id_rsa.{key}'.format(
        ssh_dir=SSH_DIR, key=KEYPAIR_NAME))
EXTERNAL_NETWORK_NAME = "ext-net"
GOOGLE_DNS_SERVER_IP = "8.8.8.8"
IDOL_STATE = "IDOL"
WORKING_STATE = "WORKING_STATE"
FINISHED_STATE = "FINISHED_STATE"
