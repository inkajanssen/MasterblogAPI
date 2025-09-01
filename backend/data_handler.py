import json
import os.path

DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(DIR, "post_data.json")


def load_posts():
    """
    Load the Json Data
    :return:
    """
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_post(entry:dict):
    """
    Saves a new post at the end of the JSON data
    :param entry:
    :return:
    """
    post_data = load_posts()
    post_data.append(entry)

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(post_data, file)


def delete_post(entry:dict):
    """
    Saves after deleting a post
    :param entry:
    :return:
    """
    posts_data = load_posts()
    posts_data = [post for post in posts_data if entry.get('id') != post.get('id')]

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(posts_data, file)


def update_post(entry:dict):
    post_data = load_posts()
    for post in post_data:
        if post.get('id') == entry.get('id'):
            post.update(entry)
            break

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(post_data, file)


def find_post_by_id(post_id):
  """ Find the book with the id `book_id`.
  If there is no book with this id, return None. """
  post_data = load_posts()
  for post in post_data:
      if post_id == post.get('id'):
          return post
  return None


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True
