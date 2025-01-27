from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def proxy():
    url = request.args.get('url')  # URL передаётся как параметр
    if not url:
        return "URL параметр не найден", 400

    # Выполняем запрос к указанному URL
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return f"Ошибка при обработке запроса: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

