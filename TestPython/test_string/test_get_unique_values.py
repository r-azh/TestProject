from pprint import pprint
import re

__author__ = 'R.Azh'


permissions = [
        "place.add_exchange",
        "admin.add_logentry",
        "device.change_mibmap",
        "profiles.add_virtualprofile",
        "place.add_site",
        "oauth2_provider.add_accesstoken",
        "profiles.delete_serviceprofile",
        "sessions.delete_session",
        "profiles.change_virtualprofile",
        "oauth2_provider.change_grant",
        "oauth2_provider.delete_grant",
        "profiles.read_virtualprofile",
        "contenttypes.delete_contenttype",
        "device.full_access_networkdevice",
        "device.add_networkdevice",
        "oauth2_provider.change_accesstoken",
        "place.delete_exchange",
        "profiles.delete_virtualprofile",
        "oauth2_provider.change_refreshtoken",
        "device.delete_interface",
        "contenttypes.add_contenttype",
        "place.full_access_province",
        "device.change_interface",
        "profiles.full_access_virtualprofile",
        "user.add_login",
        "place.change_exchange",
        "network.change_port",
        "oauth2_provider.delete_refreshtoken",
        "sessions.change_session",
        "user.read_user",
        "device.delete_networkdevice",
        "user.full_access_user",
        "network.read_port",
        "place.read_city",
        "sessions.add_session",
        "user.change_login",
        "device.delete_mibmap",
        "auth.full_access_group",
        "place.read_province",
        "network.delete_port",
        "user.delete_login",
        "place.change_province",
        "profiles.read_serviceprofile",
        "network.full_access_port",
        "oauth2_provider.add_grant",
        "device.read_mibmap",
        "profiles.change_serviceprofile",
        "profiles.add_serviceprofile",
        "place.delete_site",
        "oauth2_provider.delete_accesstoken",
        "admin.change_logentry",
        "oauth2_provider.delete_application",
        "oauth2_provider.change_application",
        "network.full_access_networkelement",
        "profiles.full_access_serviceprofile",
        "place.read_exchange",
        "post.change_comment",
        "auth.change_group",
        "post.add_comment",
        "user.delete_user",
        "place.delete_city",
        "device.read_networkdevice",
        "device.add_mibmap",
        "device.read_interface",
        "admin.delete_logentry",
        "device.change_networkdevice",
        "auth.change_permission",
        "network.delete_networkelement",
        "place.change_city",
        "place.delete_province",
        "auth.read_group",
        "place.add_province",
        "auth.delete_group",
        "network.add_networkelement",
        "place.read_site",
        "post.delete_comment",
        "oauth2_provider.add_refreshtoken",
        "device.full_access_mibmap",
        "place.full_access_site",
        "oauth2_provider.add_application",
        "place.full_access_exchange",
        "contenttypes.change_contenttype",
        "user.change_user",
        "user.add_user",
        "auth.add_group",
        "network.read_networkelement",
        "device.full_access_interface",
        "device.add_interface",
        "place.change_site",
        "network.change_networkelement",
        "network.add_port",
        "auth.delete_permission",
        "place.add_city",
        "place.full_access_city",
        "auth.add_permission"
    ]

unique_permissions = {}
for p in permissions:
    l = p.split('.')
    l2 = l[1].rsplit('_', 1)
    print(re.split('\W+|_', p))
    if l[0] not in unique_permissions:
        unique_permissions[l[0]] = {'accesses': set(),
                                    'assets': set(),
                                    'combinations': set()}
    else:
        unique_permissions[l[0]]['accesses'].add(l2[0])
        unique_permissions[l[0]]['assets'].add(l2[1])
        unique_permissions[l[0]]['combinations'].add(l[1])

pprint(unique_permissions)
