import random
import re
import string


def clear(s):
    return re.sub("[() -]", "", s)


def prepare_link(link):
    link_lo = link.lower()
    return link_lo if link_lo.startswith("http") or not link_lo else f"http://{link_lo}"


def merge_phones_like_on_homepage(contact):
    return "\n".join(filter(lambda x: x != "",
                            map(lambda s: clear(s),
                                filter(lambda x: x is not None,
                                       [contact.home_phone, contact.mobile_phone, contact.work_phone,
                                        contact.secondary_phone]))))


def merge_emails_like_on_homepage(contact):
    return "\n".join(filter(lambda x: x != "",
                            filter(lambda x: x is not None,
                                   [contact.email, contact.email2, contact.email3])))


def random_string(prefix, maxlen, symbols=None):
    symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10 if symbols is None else symbols
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def random_phone(maxlen):
    symbols = string.digits + "-" * 3
    plus = _get_symbol_or_empty_("+")
    result = plus + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
    result = result[:-1] if len(result) > maxlen else result
    return result


def _get_symbol_or_empty_(symbol):
    return random.choice([symbol, ''])


def random_site(maxlen):
    domain = random.choice(["com", "ru", "net", "edu"])
    prefix = _get_symbol_or_empty_("www.")
    http = _get_symbol_or_empty_("http://")
    symbols = string.ascii_letters + string.digits
    name = "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
    result = f"{http}{prefix}{name}.{domain}"
    len_res = len(result)
    if len_res > maxlen:
        to_del = len_res - maxlen
        result = f"{prefix}{name[:-to_del]}.{domain}"
    return result


def random_email(maxlen):
    domain = random.choice(["com", "ru", "net", "edu"])
    symbols = string.ascii_letters + string.digits
    prefix = "".join([random.choice(symbols) for i in range(random.randrange(maxlen // 2))])
    name = "".join([random.choice(symbols) for i in range(random.randrange(maxlen // 2))])
    result = f"{prefix}@{name}.{domain}"
    len_res = len(result)
    if len_res > maxlen:
        to_del = len_res - maxlen
        result = f"{prefix}@{name[:-to_del]}.{domain}"
    return result
