from flask import Flask, jsonify, request
from flask_cors import CORS

from data_handler import load_posts, validate_post_data, save_post, find_post_by_id, delete_post_from_data, update_post_in_data

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = load_posts()

    sort = request.args.get('sort', 'title')
    direction = request.args.get('direction', 'asc')

    valid_sorts = ['title', 'content']
    if sort not in valid_sorts:
        sort = 'title'

    valid_directions = ['asc', 'desc']
    if direction not in valid_directions:
        direction = 'asc'

    posts.sort(key=lambda post: post[sort])
    if direction == 'desc':
        posts.reverse()

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

    if posts:
        new_id = max(post['id'] for post in posts) + 1
    else:
        new_id = 1
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
        return jsonify('The Post was not found'), 404

    delete_post_from_data(post)

    return f"Post with id {id} has been deleted successfully.", 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify('The Post was not found'), 404

    new_post = request.get_json()
    new_post['id'] = id
    update_post_in_data(new_post)

    return jsonify(new_post)


@app.route('/api/posts/search', methods=['GET'])
def search_for_post():
    posts = load_posts()
    results = []

    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    if not title_query and not content_query:
        return "No post fits the query", 404

    for post in posts:
        post_title = post.get('title', '').lower()
        post_content = post.get('content', '').lower()

        if ((title_query and title_query in post_title)
                or (content_query and content_query in post_content)):
            results.append(post)

    if not results:
        return "No post was found", 404

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
