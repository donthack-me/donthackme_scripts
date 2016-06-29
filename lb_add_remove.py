"""Helper function to add/remove nodes from loadbalancer."""
# Copyright 2016 Russell Troxel
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import pyrax
import argparse

parser = argparse.ArgumentParser(description='Add or remove nodes from lb.')
parser.add_argument('--loadbalancer', '-l', dest='loadbalancer', required=True,
                    help='loadbalancer to edit.')
parser.add_argument('--ip_address', '-i', dest="ip", required=True,
                    help='ip address to add.')
parser.add_argument('--region', '-r', dest="region", required=True,
                    help='The rackspace region for the the request.')
parser.add_argument('--username', '-u', dest="username", required=True,
                    help='Rackspace Username.')
parser.add_argument('--api-key', '-k', dest="api_key", required=True,
                    help='Rackspace API Key.')
parser.add_argument('--remove', '-d', dest="remove", action='store_true',
                    help='remove the specified node from the loadbalancer.')
args = parser.parse_args()

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region(args.region)
pyrax.set_credentials(
    args.username,
    args.api_key
)

clb = pyrax.connect_to_cloud_loadbalancers(args.region.upper())

lb = clb.get(args.loadbalancer)
if args.remove:
    try:
        node = [node for node in lb.nodes
                if node.address == args.ip]
        node.delete()
    except Exception as e:
        msg = "Failed to remove instance {0} from LB {1}: {2}"
        print(msg.format(args.instance, args.loadbalancer, e))
        sys.exit(1)
else:
    try:
        lb.add_nodes(
            [
                clb.Node(address=args.ip, port=443, condition="ENABLED")
            ]
        )
    except Exception as e:
        msg = "Failed to add instance {0} to LB {1}: {2}"
        print(msg.format(args.ip, args.loadbalancer, e))
        sys.exit(1)
