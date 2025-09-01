from flask import Flask, jsonify, request
from flask_cors import CORS

from ..data import load_posts, validate_post_data

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = load_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    API endpoint to add a new blog post
    Expect a JSON object
    :return:
    """
    posts = load_posts()
    new_post = request.get_json()

    if not validate_post_data(new_post):
        return jsonify({"error": "Invalid post data"}), 400

    new_id=max(post['id'] for post in posts) +1
    new_post['id'] = new_id

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
