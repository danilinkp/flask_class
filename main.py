from flask import Flask, url_for, request, render_template, Blueprint, make_response, jsonify
from werkzeug.utils import redirect

from data import db_session, news_api
from data.news import News
from data.users import User
from forms.loginform import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/training/<prof>')
def training(prof):
    params = {'title': 'Тренировки в полёте',
              'prof': prof}
    return render_template('training.html', **params)


@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html', number=2)


@app.route('/auto_answer')
@app.route('/answer')
def answer():
    params = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', **params)


@app.route('/news')
def news():
    news_list = {
        "news": [
            {
                "title": "Сегодня хорошая погода",
                "content": "Невероятно, сегодня хорошая погода"
            },
            {
                "title": "Завтра хорошая погода",
                "content": "С ума сойти, и завтра хорошая погода"
            },
            {
                "title": "Послезавтра дождь",
                "content": "Все вошло в норму"
            }
        ]
    }
    return render_template('news.html', news=news_list)


@app.route('/list_prof/<list>')
def list_prof(list):
    params = {'title': 'Список профессий',
              'list': list,
              'profs': ["инженер-исследователь", "пилот", "строитель", "экзобиолог", "врач",
                        "инженер по терраформированию",
                        "климатолог", "специалист по радиационной защите", "астрогеолог",
                        "гляциолог",
                        "инженер жизнеобеспечения", " метеоролог", "оператор марсохода",
                        "киберинженер", "штурман",
                        "пилот дронов"]
              }
    return render_template('list_prof.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/que")
def que():
    return render_template('que.html', title="Пример очереди")


@app.route("/index")
def index2():
    return "<h1>И на Марсе будут яблони цвести!</h1>"


@app.route("/promotion")
def promotion():
    return f"""Человечество вырастает из детства.<br>
Человечеству мала одна планета.<br>
Мы сделаем обитаемыми безжизненные пока планеты.<br>
И начнем с Марса!<br>
Присоединяйся!"""


@app.route("/image_mars")
def image_mars():
    return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <title>Привет, Марс!</title>
                          </head>
                          <body>
                            <h1>Жди нас, Марс!</h1>
                            <img src="{url_for('static', filename='img/mars.png')}" alt="здесь должна была быть картинка, но не нашлась">
                            <div>Вот она какая, красная планета</div>
                          </body>
                        </html>"""


@app.route("/promotion_image")
def promotion_image():
    return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                            <title>Колонизация</title>
                          </head>
                          <body>
                            <h1>Жди нас, Марс!</h1>
                            <img src="{url_for('static', filename='img/mars.png')}" alt="здесь должна была быть картинка, но не нашлась">
                            <div class="alert alert-dark" role="alert">
                                Человечество вырастает из детства.
                            </div>
                            <div class="alert alert-success" role="alert">
                                Человечеству мала одна планета.
                            </div>
                            <div class="alert alert-secondary" role="alert">
                                Мы сделаем обитаемыми безжизненные пока планеты.
                            </div>
                            <div class="alert alert-warning" role="alert">
                                И начнем с Марса!
                            </div>
                            <div class="alert alert-danger" role="alert">
                               Присоединяйся!
                            </div>
                          </body>
                        </html>"""


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1>Анкета претендента</h1>
                            <h2>на участие в миссии</h2>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" placeholder="Введите фамилию" name="surname">
                                    <input type="text" class="form-control" placeholder="Введите имя" name="name"><br>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>Начальное</option>
                                          <option>Среднее</option>
                                          <option>Среднее профессиональное</option>
                                          <option>Высшее</option>
                                        </select>
                                    </div>
                                    <br>
                                    <div>Какие у Вас есть профессии?</div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="engeener_1">
                                        <label class="form-check-label" for="engeener_1">
                                            Инженер-исследователь
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="engeener_2">
                                        <label class="form-check-label" for="engeener_2">
                                            Инженер-строитель
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="pilot">
                                        <label class="form-check-label" for="pilot">
                                            Пилот
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="meteorolog">
                                        <label class="form-check-label" for="meteorolog">
                                            Метеоролог
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="engeener_3">
                                        <label class="form-check-label" for="engeener_3">
                                            Инженер по жизнеобеспечению
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="engeener_4">
                                        <label class="form-check-label" for="engeener_4">
                                            Инженер по радиационной защите
                                        </label>
                                    </div>
                                    
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="doctor">
                                        <label class="form-check-label" for="doctor">
                                            Врач
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="" id="Exobiologist">
                                        <label class="form-check-label" for="Exobiologist">
                                            Экзобиолог
                                        </label>
                                    </div>
                                    <br>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <br>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <br>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <br>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                                    </div>
                                    <br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['surname'])
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['class'])
        print(request.form['sex'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        return "Форма отправлена"


@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f"""<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <link rel="stylesheet" 
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                            crossorigin="anonymous">
                                <title>Варианты выбора</title>
                              </head>
                              <body>
                                <h1>Мое предложение: {planet_name}</h1>
                                <h2>Эта планета близка к земле;</h2>
                                <div class="alert alert-success" role="alert">
                                    На ней много необходимых ресурсов;
                                </div>
                                <div class="alert alert-secondary" role="alert">
                                    На ней есть вода и атмосфера;
                                </div>
                                <div class="alert alert-warning" role="alert">
                                    На ней есть небольшое магнитное поле;
                                </div>
                                <div class="alert alert-danger" role="alert">
                                    Наконец, она просто красива!
                                </div>
                              </body>
                            </html>"""


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f"""<!doctype html>
                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <link rel="stylesheet" 
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                                crossorigin="anonymous">
                                    <title>Результаты</title>
                                  </head>
                                  <body>
                                    <h1>Результаты отбора</h1>
                                    <h2>Претендента на участие миссии {nickname}:</h2>
                                    <div class="alert alert-success" role="alert">
                                        Поздравляем! Ваш рейтинг после {level} этапа отбора
                                    </div>
                                    <h3>составляет {rating}!</h3>
                                    <div class="alert alert-warning" role="alert">
                                        Желаем удачи!
                                    </div>
                                  </body>
                                </html>"""


@app.route('/load_photo')
def load_photo():
    if request.method == 'GET':
        return f'''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                    crossorigin="anonymous">
                                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                    <title>Пример формы</title>
                                  </head>
                                  <body>
                                    <h1>Загрузка фотографии</h1>
                                    <h2>для участия в миссии</h2>
                                    <div>
                                        <form class="login_form" method="post">
                                            <div class="form-group">
                                                <label for="photo" method="get">Приложите фотографию</label>
                                                <input type="file" class="form-control-file" id="photo" name="file">
                                            </div>
                                            <button type="submit" class="btn btn-primary">Записаться</button>
                                        </form>
                                    </div>
                                  </body>
                                </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        print(f.read())
        return "Форма отправлена"


@app.route('/sample_file_upload', methods=['POST', 'GET', 'PATCH'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input method="patch" type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        print(f.read())
        return "Форма отправлена"


#
# def user_add():
#     user = User()
#     user.name = "Пользователь 1"
#     user.about = "биография пользователя 1"
#     user.email = "email@email.ru"
#     user.set_password("123456")
#
#     user2 = User(name="Пользователь 2",
#                  about="биография пользователя 2",
#                  email="email2@email.ru")
#     user2.set_password("1234")
#
#     db_sess = db_session.create_session()
#     db_sess.add(user)
#     db_sess.add(user2)
#     db_sess.commit()
#
#
# def user_get():
#     db_sess = db_session.create_session()
#     user = db_sess.query(User).filter(User.id == 1).first()
#     for news in user.news:
#         print(news.created_date)
#
#
# def news_add():
#     db_sess = db_session.create_session()
#
#     news = News(title="Первая новость", content="Привет блог!",
#                 user_id=1, is_private=False)
#     user = db_sess.query(User).filter(User.email == "email@email.ru").first()
#     news2 = News(title="Вторая новость", content="Уже вторая запись!",
#                  user=user, is_private=False)
#
#     news3 = News(title="Вторая новость", content="Уже вторая запись!",
#                  user_id=2, is_private=False)
#
#     db_sess.add(news)
#     db_sess.add(news2)
#     db_sess.add(news3)
#     db_sess.commit()
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_add()
    # user_get()
    # news_add()
    app.register_blueprint(news_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
