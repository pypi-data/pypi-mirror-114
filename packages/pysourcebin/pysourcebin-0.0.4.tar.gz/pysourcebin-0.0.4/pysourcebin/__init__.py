import requests as request
import re


def get_url(key: str):
  return f"https://sourceb.in/{key}"

def get_key(url):
  a = re.findall('https?://(sourceb\.in|srcb\.in)\/(.+)', url)
  return a[0][1]

def create(name: str, code: str, title="None", description="None"):
  res = request.post("https://sourceb.in/api/bins/", json={
        'title': title, 'description': description,
				'files': [ { "name": name, "content": code } ],
			})
  data = res.json()
  return get_url(data['key'])

def read_key(key: str):
  main = request.get(f"https://sourceb.in/api/bins/{key}", headers={ "ACCEPT": 'application/json'})
  if not main.ok:
    raise NameError("key must be a key to an existing sourcebin")
  else:
    answer: list[str] = []
    main_data = main.json()
    size: int = len(main_data['files'])
    for i in range(size):
      res = request.get(f"https://cdn.sourceb.in/bins/{key}/{i}")
      answer.append(res.text)
    return {
      'code': answer,
      'fileCount': size,
      'createdAt': main_data['created'],
      'key': main_data['key']
      }

def read_url(url: str):
  key = get_key(url)
  main = request.get(f"https://sourceb.in/api/bins/{key}", headers={ "ACCEPT": 'application/json'})
  if not main.ok:
    raise NameError("key must be a key to an existing sourcebin")
  else:
    answer: list[str] = []
    main_data = main.json()
    size: int = len(main_data['files'])
    for i in range(size):
      res = request.get(f"https://cdn.sourceb.in/bins/{key}/{i}")
      answer.append(res.text)
    return {
      'code': answer,
      'fileCount': size,
      'createdAt': main_data['created'],
      'key': main_data['key']
      }
