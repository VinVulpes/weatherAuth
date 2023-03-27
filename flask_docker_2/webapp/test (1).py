from flask import Flask
app = Flask(__name__)
def checkAuth():
    # Возвращаем значение
    return 'Some text'
@app.route('/')
def function1():
    # Вызываем функцию 2
    temp = checkAuth()

    # Используем результат из функции 2
    print(temp)
    return temp


# Вызываем функцию 1
function1()
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)








    # try:
    #     user_name = (request.headers['User-Name'])
    # except KeyError:
    #     return 'Bad request, the User-Name header is missing'
    #отправка сообщений серверу аутентификации
    #if request == False
    #    return False
    #else:
    #   return True