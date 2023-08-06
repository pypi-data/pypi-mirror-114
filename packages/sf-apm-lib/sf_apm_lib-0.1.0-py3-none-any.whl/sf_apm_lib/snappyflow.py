from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES
import json

__CP_ENCRYPTED_KEY = "U25hcHB5RmxvdzEyMzQ1Ng=="

def get_trace_config(profile_key, project_name, app_name):
    """ Returns Snappyflow trace config

    Args:
        profile_key ([string]): [Snappyflow Profile Key]
        project_name ([string]): [Project name]
        app_name ([string]): [App name]

    Raises:
        ValueError: [If profile key is invalid]

    Returns:
        [dict]: [trace config]
    """    

    unpad = lambda s : s[0:-ord(s[-1:])]

    key = base64.b64decode(__CP_ENCRYPTED_KEY)
    
    enc = base64.b64decode(profile_key)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    message = unpad(cipher.decrypt( enc[16:] )).decode('utf-8')
    try:
        data = json.loads(message)
        global_labels = "_tag_projectName={},_tag_appName={},_tag_profileId={}".format(project_name, app_name, data['profile_id'])
        trace_data = {
            'SFTRACE_SERVER_URL': data['trace_server_url'],
            'SFTRACE_SPAN_FRAMES_MIN_DURATION': "1ms",
            'SFTRACE_STACK_TRACE_LIMIT': 2,
            'SFTRACE_CAPTURE_SPAN_STACK_TRACES': False,
            'SFTRACE_VERIFY_SERVER_CERT': False,
            'SFTRACE_GLOBAL_LABELS': global_labels
        }
        return trace_data
    except Exception as e:
        raise ValueError("Invalid profile key.")