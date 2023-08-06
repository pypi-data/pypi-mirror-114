from faker import Faker
from faker.providers import BaseProvider
import random
import logging
import time


class MyFaker(object):

    def __init__(self, fake_map=None):
        # 如果要关联到已存在的规则使用fake_map
        self.fake_map = {"phone": "phone_number"}
        self.fake = Faker()

    def add_provider(self, provider: BaseProvider):
        self.fake.add_provider(provider)

    def add_fake_map(self, pos: dict = None, **kwargs):
        if pos:
            self.fake_map.update(pos)
        self.fake_map.update(**kwargs)

    def create_string(self, param, **identity):
        name = param.param.real_name
        if getattr(self, name.lower()):
            return getattr(self, name.lower())
        if identity.get("is_random", False):
            str_len = identity.get("string_len", 5)
            return "_".join([name, create_num_string(str_len)])
        elif identity.get("num"):
            return "_".join([name, str(identity.get("num"))])
        else:
            return name

    def __getattr__(self, item):
        if item == "password":
            return self.fake.password(special_chars=False)
        try:
            return getattr(self.fake, item)()
        except AttributeError:
            try:
                return getattr(self.fake, self.fake_map[item])()
            except KeyError:
                logging.debug("fake_map 不存在 %s" % item)
            except AttributeError:
                logging.debug("fake_map %s 的对应不对" % item)
        return "_".join([item, create_num_string(5)])


fake = MyFaker()


def create_num_string(num, prefix=None):
    samples = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
               'e', 'd', 'c', 'b', 'a', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]

    if prefix:
        return prefix + ''.join(random.sample(samples, num))
    return ''.join(random.sample(samples, num))


def create_timestamp(delay=0, before=0):
    return int(time.time() * 1000) + delay * 60 * 1000 - before * 60 * 1000
