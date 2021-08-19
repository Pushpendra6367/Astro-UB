from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest,UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from astro.utils import admin_cmd

async def get_full_user(event):
     args = event.pattern_match.group(1).split(":", 1)
     extra = None
     if event.reply_to_msg_id and not len (args) == 2:
       previous_message = await event.get_reply_message()
       user_obj = await event.client.get_entity(previous_message.from_id)
       extra = event.pattern_match.group(1)
     elif len(args[0]) > 0:
          user = args[0]
          if len(args) == 2:
           extra = args[0]
           if user.isnumeric():
              user = int(user)
           if not user:
              await event.edit("`ITS not possible without user id bach gaya noob`")
              return
           if event.message.entities is not None:
              probable_user_mention_entity = event.message.entities[0]
              if isinstance(probable_user_mention_entity,MessageMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
              try:
                user_obj = await event.client.get_entity(user)
              except Exception as err:
                  return await event.edit("Error... Please report at @Astro_HelpChat", str(err)
            )
                  return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

  
  
@astro.on(admin_cmd(pattern="gban ?(.*)"))
async def gben(astro):
    dc = astro
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("Gbanning This User !")
    else:
        dark = await dc.edit("Wait Processing.....")
    me = await astro.client.get_me()
    await dark.edit(f"Trying to ban you globally..wait  you nub nibba")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await astro.get_chat()
    a = b = 0
    if astro.is_private:
        user = astro.chat
        reason = astro.pattern_match.group(1)
    else:
        astro.chat.title
    try:
        user, reason = await get_full_user(astro)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        return await dark.edit(f"**Something W3NT Wrong 🤔**")
    if user:
        if user.id == 1258905497:
            return await dark.edit(f"**You nub nibba..I can't gban my dev..**")
        try:
            from userbot.plugins.sql_helper.gmute_sql import gmute
        except:
            pass
        try:
          await astro.client(BlockRequest(user))
        except:
            pass
        testastro = [
            d.entity.id
            for d in await astro.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testastro:
            try:
                await astro.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(f"**Globally banned 🙄🙄 Total Affected Chats **: `{a}`")
            except:
                b += 1
    else:
        await dark.edit(f"**Reply to a user you dumbo !!**")
    try:
        if gmute(user.id) is False:
            return await dark.edit(f"**Error! User already gbanned.**")
    except:
        pass
    return await dark.edit(
        f"**Globally banned this nub nibba [{user.first_name}](tg://user?id={user.id}) Affected Chats😏 : {a} **"
    )
 

@astro.on(admin_cmd(pattern="ungban ?(.*)"))
async def gunben(userbot):
    dc = astro
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("`Wait Let Me ungban this nub nibba again😂`")
    else:
        dark = await dc.edit("Weit nd watch ! ")
    me = await astro.client.get_me()
    await dark.edit(f"Trying To Ungban User !")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await astro.get_chat()
    a = b = 0
    if astro.is_private:
        user = astro.chat
        reason = astro.pattern_match.group(1)
    else:
        astro.chat.title
    try:
        user, reason = await get_full_user(astro)
    except:
        pass
        try:
           if not reason:
            reason = "Private"
        except:
            return await dark.edit("Someting Went Wrong 🤔")
    if user:
        if user.id == 1258905497:
            return await dark.edit(
                "**You nub nibba..can't gban or ungban my dev... !**"
            )
        try:
            from astro.plugins.sql_helper.gmute_sql import ungmute
        except:
            pass
        try:
            await astro.client(UnblockRequest(user))
        except:
            pass
        testastro = [
            d.entity.id
            for d in await astro.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testastro:
            try:
                await astro.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await dark.edit(f"**Ungbaning this nub nibba.. AFFECTED CHATS - {a} **")
            except:
                b += 1
            else:
              await dark.edit("**Reply to a user you dumbo**")
    try:
        if ungmute(user.id) is False:
            return await dark.edit("**Error! User already ungbanned.**")
    except:
        pass
    return await dark.edit(
        f"**Ungbanned this noon nibba..ja chod diya agli baar mardenge teri... ; USER - [{user.first_name}](tg://user?id={user.id}) CHATS : {a} **"
    )


@astro.on(ChatAction)
async def handler(rkG):
    if rkG.user_joined or rkG.user_added:
        try:
            from astro.plugins.sql_helper.gmute_sql import is_gmuted

            guser = await rkG.get_user()
            gmuted = is_gmuted(guser.id)
        except:
            return
        if gmuted:
            for i in gmuted:
                if i.sender == str(guser.id):
                    chat = await rkG.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                          await client.edit_permissions(
                                rkG.chat_id, guser.id, view_messages=False
                            )
                          await rkG.reply(
                                f"**Gbanned User(the ultimate chutiya) Joined the chat!!** \n"
                                f"**Victim Id**: [{guser.id}](tg://user?id={guser.id})\n"
                                f"**Action **  : `Banned this nub nibba again...Sed`"
                            )
                        except:
                            rkG.reply(
                                "`No Permission To Ban.. @admins please ban him he is a globally banned user and a potential spammer...!`"
                            )
                            return
