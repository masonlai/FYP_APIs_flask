from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, sys
from flask_cors import CORS

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/', methods=["GET"])
def hello():
    return jsonify({
        "api_version": "1.0",
        "api_base_url": "http://example.com/api/v1",
        "current_user_url": "http://example.com/api/v1/user",
        "authentication_url": "http://example.com/api/v1/token",
    })

from login import login

if __name__ == '__main__':
  app.run(debug=True)
