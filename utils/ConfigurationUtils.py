from Crypto.Util.number import size
from dateutil.parser import parser

__author__ = 'zanetworker'

from ConfigParser import SafeConfigParser
import utils.CommonUtils as CommonUtil


parser = SafeConfigParser()

try:
    config_file = CommonUtil.get_file_location('config', 'deployment.ini')
    parser.read(config_file)

except Exception as e:
    print e.message


def load_vipr_credentials():

    results = {
        'vipr_host': parser.get('vipr', 'HOST'),
        'vipr_port': parser.get('vipr', 'PORT', 4443),
        'cookie_path': parser.get('vipr', 'COOKIE_DIR_ABS_PATH')
    }
    return results


def load_smis_details():

    results = {
        'ip_address': parser.get('smis','IP_ADDRESS'),
        'name': parser.get('smis', 'NAME'),
        'password': parser.get('smis', 'PASS'),
        'port_number': parser.get('smis', 'PORT'),
        'use_ssl': parser.get('smis', 'USE_SSL'),
        'user_name': parser.get('smis', 'USER')
    }
    return results

def load_vplex_details():
    results = {
        "ip_address": parser.get('vplex','IP_ADDRESS'),
        "name": parser.get('vplex', 'NAME'),
        "password": parser.get('vplex', 'PASS'),
        "port_number": parser.get('vplex', 'PORT'),
        "use_ssl": parser.get('vplex', 'USE_SSL'),
        "user_name": parser.get('vplex', 'USER'),
        "interface_type": parser.get('vplex', 'INTERFACE_TYPE')
    }
    return results


def load_cmcne_details():
    results = {
        "name": parser.get('cmcne','NAME'),
        "system_type": parser.get('cmcne', 'SYSTEM_TYPE'),
        "smis_provider_ip": parser.get('cmcne', 'SMIS_IP'),
        "smis_port_number": parser.get('cmcne', 'SMIS_PORT'),
        "smis_user_name": parser.get('cmcne', 'SMIS_USER'),
        "smis_password": parser.get('cmcne', 'SMIS_PASSWORD'),
        "smis_use_ssl": parser.get('cmcne', 'USE_SSL')
    }
    return results

def load_hosts_details():
    host_names = parser.get('hosts','HOST_NAME').split(',')
    names = parser.get('hosts', 'NAME').split(',')
    user_names = parser.get('hosts', 'USER_NAME').split(',')
    passwords = parser.get('hosts', 'PASSWORD').split(',')
    use_ssls = parser.get('hosts', 'USE_SSL').split(',')
    types = parser.get('hosts', 'TYPE').split(',')
    port_numbers = parser.get('hosts','PORT_NO').split(',')

    results = []
     #TODO - CHeck that all arrays are of the same size
    for i in range(0, len(host_names)):
        results.append({
            "host_name": host_names[i],
            "name": names[i],
            "user_name": user_names[i],
            "password": passwords[i],
            "port_number": port_numbers[i],
            "use_ssl": use_ssls[i],
            "type": types[i]
        })

    return results