
from importlib import resources
from configparser import ConfigParser
import connecty, discord, string
import colorama
import types
colorama.init()

CBLUE = "\33[34m"
CVIOLET = "\33[35m"
CEND = "\033[0m"
CBOLD = "\033[1m"

def wrap(cl):
    def fu(txt):
        return cl + txt + CEND
    return fu

print(wrap(CBLUE)("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"))
print(wrap(CBLUE)("▉") + CBOLD + " JOIN THE SUPPORT SERVER FOR HELP!! https://discord.gg/fcZBB2v " + wrap(CBLUE)("█"))
print(wrap(CBLUE)("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█"))

args = connecty.parser.parse_args()
config = ConfigParser()
config.read_string(resources.read_text(connecty, "defaults.ini"))
config.read(args.config)
bot = connecty.Bot()
bot_config = dict(config["BOT"])
del config["BOT"]
connecty.GB.bot = bot

@bot.configure
async def init():
    for sec in config.sections():
        sec = config[sec]
        await bot.register(list(int(ids) for ids in sec["channels"].split()))


def start(): bot.run(bot_config["token"])
if __name__ == "__main__": start()