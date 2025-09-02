from flask import Flask, jsonify, request
from flask_cors import CORS

from data_handler import load_posts, validate_post_data, save_post, find_post_by_id, delete_post

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

    save_post(new_post)

    return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    An API endpoint that will allow clients to delete a post by its id
    :param id:
    :return:
    """
    post = find_post_by_id(id)

    if post is None:
        return 'The Post was not found', 404

    delete_post(post)

    return f"Post with id {id} has been deleted successfully.", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
