import logging
import sys
import telegram
import yaml

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

with open('bender.yaml', 'r') as f:
    config = yaml.load(f)

TOKEN = config['token']

bot = telegram.Bot(token=TOKEN)

# TODO Determine the chat ID programmatically
# chat_id = bot.getUpdates()[-1].message.chat_id
chat_id = ***REMOVED***
# chat_id = '@pppschmitt'

bot.sendMessage(chat_id=chat_id, text=sys.argv[1])
