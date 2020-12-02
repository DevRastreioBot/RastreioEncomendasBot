import json

import requests

class TelegramBot:
    def __init__(self, token):
        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.nova_mensagem_listener_func = None
        self.nova_mensagem_listener_func = None

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    if self.nova_mensagem_listener_func is not None:
                        self.nova_mensagem_listener_func(chat_id, mensagem, primeira_mensagem)

    def add_nova_mensagem_listener(self, func):
        self.nova_mensagem_listener_func = func

    # Obtendo as mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def responder(self, chat_id, resposta):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)
