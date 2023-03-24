from flask import Flask, jsonify, request
import logging


app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename='log.log'
)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)


    logging.info(f'Response: {response!r}')
    
    return jsonify(response)


def handle_dialog(req, resp):
    user_id = req['session']['user_id']
    
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                'Не хочу',
                'Не буду',
                'Отстань!'
            ]
        }
        resp['response']['text'] = 'Привет! Купи слона!'
        resp['response']['buttons'] = get_suggests(user_id)
        return
    
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        resp['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        resp['response']['end_session'] = True
        return
    resp['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    resp['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
