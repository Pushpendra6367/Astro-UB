from astro.config import Config 
from astro import bot 
from astro import vision 

BOT_USERNAME = Config.BOT_USERNAME
OWNER_USERNAME = Config.OWNER_USERNAME
ASTRO = "@Astro_UserBot"
# Oh Yes...
if Config.SUDO_USERS:
    sudo = "YES Have Sudo"
else:
    sudo = "Nope No Sudo"
if Config.PMSECURITY.lower() == "off":
    pm = "DE-ACTIVE"
else:
    pm = "ACTIVE"

astro = f"**ƛsτʀ๏ Vision:** {vision}\n"
astro += f"**SUDO USERS:** {sudo}\n"
astro += f"**PM SECURITY:** {pm}\n"
astro += f"**Assistant:** {BOT_USERNAME}\n"
astro += f"__My Master__: {OWNER_USERNAME}\n"
astro += f"__Protected by__: {ASTRO}\n\n"

astrostats = f"{astro}"


# FOR PING LITTLE SETUP 
ASTRO = bot.me.first_name
OWNER_ID = bot.me.id

# PYTHON VISION 
PYTHON = "3.9.6"
