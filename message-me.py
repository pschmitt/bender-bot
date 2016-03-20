from bender.config import get_config_section
import os
import logging
import sys
import telegram

os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/bender')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = telegram.Bot(token=get_config_section(section='bot')['token'])

# TODO Determine the chat ID programmatically
# chat_id = bot.getUpdates()[-1].message.chat_id
# chat_id = '@pppschmitt'
with open('../chat_id.txt', 'r') as f:
    chat_id = f.read()

bot.sendMessage(chat_id=chat_id, text=sys.argv[1])
