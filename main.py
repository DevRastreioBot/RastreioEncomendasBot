from correios import Correios
from telegram import TelegramBot

bot = TelegramBot('1409626650:AAHTdjbu64aG23T2OaRdoBNCenrNwAzRBJk')
correios = Correios('teste', '1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f')

encomendas_cache = {}

def build_response(chat_id, mensagem, is_primeira):
    if mensagem == '/start' or is_primeira:
        return (
            '🤖💬 Bem vindo ao bot de rastreamento de encomendas. \nPara fazer um novo rastreamento, envie apenas o código (13 dígitos):')
    elif len(mensagem) != 13:
        return ('🤖💬 Quantidade de dígitos inválidos, por favor, digite apenas o código (13 dígitos):')

    rastreamento = correios.rastrear(mensagem)
   
    if rastreamento is not None and len(rastreamento["eventos"]) >0:
        ultimo_evento = rastreamento["eventos"][0]

        encomendas_cache[rastreamento["codigo"]] = {
            "status": ultimo_evento["status"],
            "chat_id":chat_id,
            "ultimo": rastreamento["ultimo"]
        }

        msg = ""
        msg += "📦Encomenda Localizada!"
        msg += "\n\n"
        msg += f'{rastreamento["codigo"]}'
        msg += "\n\n"
        msg += f'📍 Local: {ultimo_evento["local"]}\n'
        msg += f'✉️ Status: {ultimo_evento["status"]}\n'
        msg += f'🕐 Data: {ultimo_evento["data"]} {ultimo_evento["hora"]}\n\n'
        msg += '🤖💬 Para fazer um novo rastreamento, envie apenas o código (13 dígitos):'
        return msg
    else:
        return f'🤖💬Encomenda não encontrada!\nConfira seu código de rastreio, e tente novamente:'


bot.add_nova_mensagem_listener(
    lambda chat_id, mensagem, is_primeira: bot.responder(chat_id, build_response(chat_id,mensagem, is_primeira)))
bot.Iniciar()
