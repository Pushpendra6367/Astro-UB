from telethon import *

from astro import CMD_HELP

from astro.utils import admin_cmd 


# Fixed by @NOOBGeng Second Member
@astro.on(admin_cmd(pattern=r"snipe (.*)"))
async def _(dc):

    d = dc.pattern_match.group(1)

    c = d.split(" ")  

    chat_id = c[0]
    try:  
        chat_id = int(chat_id)
    
    except BaseException:  

        pass

    msg = ""
    masg = await dc.get_reply_message()  
    if dc.reply_to_msg_id:
        await borg.send_message(chat_id, masg)
        await dc.edit("Text Sniped Sucessfully")
    for i in c[1:]:
        msg += i + " "  
    if msg == "":  # hoho
        return
    try:
        await borg.send_message(chat_id, msg)
        await dc.edit("**Text Snipes Sucessfully**")
    except BaseException:  
        await dc.edit(".snipe (username) (text)")


CMD_HELP.update(
    {
        "snipe": ".snipe (username) (text)\n or\n .snipe (username)(reply to msg)\n it'll forward the replyed msg"
    }
)
