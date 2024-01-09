import asyncio
import hashlib
import os
import random
import string
from logging import getLogger
from urllib.parse import urlparse

from data import db, Link

logger = getLogger(__name__)


def chain_in_db(cute_link, link):
    try:
        db.session.add(Link(cute_link=cute_link, link=link))
        db.session.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False


def get_cute_link(link):
    cute_link = db.session.query(Link).filter_by(link=link).first()
    return cute_link.cute_link if cute_link else None


def get_original_link(cute_link):
    link_entry = db.session.query(Link).filter_by(cute_link=cute_link).first()
    return link_entry.link if link_entry else None


# LIGHT VERSION
# def create_cute_link(length=10) -> str:
#     while True:
#         string_massive = string.ascii_letters + string.digits
#         generated_link = "".join([random.choice(string_massive) for _ in range(length)])
#         if not get_original_link(generated_link):  # Проверяем уникальность
#             return generated_link


# STRONG VERSION
def create_cute_link(original_link, length=10) -> str:
    # Salt generation
    salt = os.urandom(16)
    # Creating a hash from original link and salt
    hash_object = hashlib.sha256(original_link.encode() + salt)
    return hash_object.hexdigest()[:length]


def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


if __name__ == '__main__':
    print(create_cute_link('https://google.com'))
