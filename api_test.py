from requests import get, post

print(get('http://localhost:8080/api/news').json())


print(post('http://localhost:5000/api/news',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_private': False}).json())
