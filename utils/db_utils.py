import copy
import re

from model.group import Group


def __strip__(string):
    if string is not None:
        return re.sub(' +', ' ', string.strip())
    else:
        return None


def clean_group_name(group_from_db):
    return Group(id=group_from_db.id, name=__strip__(group_from_db.name))


def clean_contact_name(contact_from_db):
    temp = copy.deepcopy(contact_from_db)
    temp.firstname = __strip__(contact_from_db.firstname)
    temp.lastname = __strip__(contact_from_db.lastname)
    temp.address = __strip__(contact_from_db.address)
    return temp
