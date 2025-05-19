from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap


@app.route('/api/id/', methods=('POST',))
def add_short_url():
    if request.content_type != 'application/json' or not request.data:
        return (jsonify({"message": "Отсутствует тело запроса"}),
                HTTPStatus.BAD_REQUEST)
    data = request.get_json()
    if not data:
        return (jsonify({"message": "Отсутствует тело запроса"}),
                HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        return (jsonify({"message": "\"url\" является обязательным полем!"}),
                HTTPStatus.BAD_REQUEST)
    url_map = URLMap()
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = url_map.get_unique_short_id()
        data['custom_id'] = custom_id
    if url_map.is_short_link_exists(custom_id):
        return (jsonify({"message": "Предложенный вариант"
                                    " короткой ссылки уже существует."}),
                HTTPStatus.BAD_REQUEST)
    if not url_map.is_valid_short_id(custom_id):
        return (jsonify({"message": "Указано"
                                    " недопустимое имя для короткой ссылки"}),
                HTTPStatus.BAD_REQUEST)
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_short_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        return (jsonify({"message": "Указанный id не найден"}),
                HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK