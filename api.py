from logging import getLogger
from typing import Any

import flask
from flask import request, Response, redirect

from config import ALCHEMY_DATABASE_URL, DOMAIN_NAME, CACHE_REDIS_URL, CACHE_TYPE
from data import db
from main import create_cute_link, chain_in_db, is_valid_url, get_cute_link, get_original_link
from flask_caching import Cache

app = flask.Flask(__name__)
logger = getLogger(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ALCHEMY_DATABASE_URL
app.config['CACHE_TYPE'] = CACHE_TYPE
app.config['CACHE_REDIS_URL'] = CACHE_REDIS_URL

db.init_app(app)
cache = Cache(app)

with app.app_context():
    db.create_all()


@app.route('/create_cute_link', methods=['POST'])
def handle_create_cute_link() -> tuple[str, int] | Any:
    link = request.form.get('link')
    if not is_valid_url(link):
        return Response('Invalid link', 400)
    
    exist_cute_link = get_cute_link(link)
    if exist_cute_link:
        return Response(f"http://{DOMAIN_NAME}/{exist_cute_link}", status=200)
    else:
        cute_link = create_cute_link(link)
        if chain_in_db(cute_link, link):
            return Response(f"http://{DOMAIN_NAME}/{cute_link}", status=201)
        else:
            return Response('Error creating link', 500)


@app.route('/<cute_link>', methods=['GET'])
@cache.cached(timeout=50)
def handle_cute_link(cute_link: str) -> tuple[str, int] | Any:
    link = get_original_link(cute_link)
    if link:
        return redirect(link)
    else:
        return Response(f"Link not found", status=400)


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


@app.errorhandler(500)
def server_error(error):
    return 'Something went wrong', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
