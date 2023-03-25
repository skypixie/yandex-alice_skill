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

    handle_dialog(request.json, response, "слона")
    handle_dialog(request.json, response, "кролика")


    logging.info(f'Response: {response!r}')
    
    return jsonify(response)


def handle_dialog(req, resp, product):
    user_id = req['session']['user_id']
    
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                'Не хочу',
                'Не буду',
                'Отстань!'
            ]
        }
        resp['response']['text'] = f'Привет! Купи {product}!'
        resp['response']['buttons'] = get_suggests(user_id)
        return
    
    for word in ['ладно', 'куплю', 'покупаю', 'хорошо']:
        if word in req['request']['original_utterance'].lower():
            resp['response']['text'] = f'{product.capitalize()} можно найти на Яндекс.Маркете!'
            resp['response']['end_session'] = True
            return
    
    resp['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи {product}!"
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
 
