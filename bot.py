#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0116

import logging
import random
import os
import telegram
from telegram.ext import Updater, CommandHandler

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ["TOKEN"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
	update.message.reply_text(f'Olá, {update.message.chat.first_name}.\n'+ \
							   'Sou um bot que faz o lançamento de '+\
							   'dados D6 para o sistema Shadowrun.\n'+\
							   'Digite sem chaves:\n/roll {Quantidade de Dados} {Nome do Lançamento (Opcional)}')

def roll(update, context):
	try:
		context.bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
		
		dice_qty, name = int(context.args[0]), " ".join(context.args[1:])

		if dice_qty > 100:
			update.message.reply_text("O número máximo de dados é 100!")
			return 1

		sucess_count = 0
		ones_count = 0  
		dices = ""
		for i in range(dice_qty):
			dice_result = random.randint(1,6)
			
			if 5 <= dice_result <= 6:
				sucess_count += 1
				formatting = f"*{dice_result}*"
			elif dice_result == 1:
				ones_count += 1
				formatting = f"_{dice_result}_"
			else:
				formatting = f"`{dice_result}`"

			dices += formatting + ", "
		
		dices = dices[:-2]
		hasFailure = ones_count >= dice_qty / 2
		
		if hasFailure and sucess_count == 0:
			failure_message = "FALHA CRÍTICA"
		elif hasFailure:
			failure_message = "FALHA"
		
		update.message.reply_markdown_v2((f'*{name}*\n' if (name != 0) else "") + \
										  f'{dices}\n\nSucessos: {sucess_count}' + \
										 (f'\n\n{failure_message}' if hasFailure else ''))
		
	except:
		update.message.reply_text("Digite sem as chaves: /roll {Quantidade de dados} {Nome do lançamento (Opcional)}")
	

def main() -> None:
	updater = Updater(TOKEN)

	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", start))
	dispatcher.add_handler(CommandHandler("roll", roll))
	
	updater.start_webhook(listen="0.0.0.0",
						  port=int(os.environ.get('PORT', 5000)),
						  url_path=TOKEN)
	updater.bot.setWebhook('https://shadowrun-dice-roller-bot.herokuapp.com/' + TOKEN) 

	updater.idle()
	

if __name__ == '__main__':
    main()