from ldap3 import Server, Connection, ALL, NTLM, SIMPLE, MODIFY_REPLACE
import os
from zou.app import config

LDAP_USER = os.getenv("LDAP_USER", "super-user")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "")

ldap_server = "%s:%s" % (config.LDAP_HOST, config.LDAP_PORT)
SSL = False
if config.LDAP_IS_AD_SIMPLE:
    user = LDAP_USER
    authentication = SIMPLE
    SSL = True
elif config.LDAP_IS_AD:
    user = f"{config.LDAP_DOMAIN}\{LDAP_USER}"
    authentication = NTLM
else:
    user = f"uid={LDAP_USER},{config.LDAP_BASE_DN}"
    authentication = SIMPLE

server = Server(ldap_server, get_info=ALL, use_ssl=SSL)
conn = Connection(
    server,
    user=user,
    password=LDAP_PASSWORD,
    authentication=authentication,
    raise_exceptions=True,
    auto_bind=True,
)

def create_ldap_user(first_name, last_name, email, password, phone='', role='Artist', active='yes'):
    """
    Connect to a LDAP server, then creates user.
    """
    common_name = f"{first_name} {last_name}"
    user_name = f"uid={first_name}-{last_name},{config.LDAP_BASE_DN}"

    conn.add(user_name, attributes={
                            'objectClass':  ['inetOrgPerson', 'posixGroup', 'person'], 
                            'cn': common_name, 'sn': last_name, 'givenName': first_name, 'mail': email, 'gidNumber': 20043,
                            'userPassword': password})
    return f"{first_name}-{last_name}".lower()
    
def update_ldap_user_password(user_name, password):
    """
    Connect to a LDAP server, then update user password.
    """
    print(user_name, '-------------------------updating---------------------------------')
    conn.modify(user_name,
         {'userPassword': [(MODIFY_REPLACE, [password])]})
    return user_name