from flask import jsonify

from .base import app
from .routes import api
from .connector import Services, fallback, MAX_FAILS, failed_requests

app.register_blueprint(api, url_prefix='/api/v1')


@app.route('/manage/health', methods=['GET'])
def health():
    return jsonify(fallback), 200
