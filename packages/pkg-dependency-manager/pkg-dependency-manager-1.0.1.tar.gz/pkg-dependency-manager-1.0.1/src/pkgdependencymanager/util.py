import os
import platform
def get_platform():
    platform_name = platform.platform().split('-')[0]
    if platform_name == "Linux":
        lsb_release = open("/etc/lsb-release", "r")
        lines = lsb_release.readlines()
        lsb_release.close()
        for line in lines:
            tokens = line.strip().split('=')
            if len(tokens) == 2:
                if tokens[0] == "DISTRIB_ID":
                    platform_name += "/" + tokens[1]
    return platform_name
def get_tree_element(path: str, tree):
    path_nodes = path.split('/')
    try:
        node = tree[path_nodes[0]]
    except KeyError:
        return None
    if len(path_nodes) == 1:
        return node
    else:
        remaining_path = path[(len(path_nodes[0]) + 1):]
        return get_tree_element(remaining_path, node)
