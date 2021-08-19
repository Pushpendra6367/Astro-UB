#Astro-UB 
# © Alone_loverboy
from os import remove, execle, path, makedirs, getenv, environ
from shutil import rmtree

import sys, os

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from astro import CMD_HELP, bot 
from astro import bot as borg
from astro.utils import admin_cmd
import asyncio
from astro.config import Config
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')

HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
GIT_REPO_NAME = "Astro-UB"
UPSTREAM_REPO_URL = "https://github.com/PsychoBots/Astro-UB"

async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "On " + "%d/%m/%y" + " at " + "%H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by **{c.author}**\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@borg.on(admin_cmd(pattern="update ?(.*)"))
async def upstream(ups):
    await ups.edit("Checking for new updates\nIf any came🤷")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_updateme = False

    try:
        txt = "`Oops.. Updater cannot continue as🥲"
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`directory {error} is not found`')
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Early failure! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await ups.edit(
                f"**Sync-Verification required since the directory {error} does not seem to be a git repository.\
                \nSync-Verify now with {GIT_REPO_NAME}\
            \nTo do This type** `.update now`."
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_updateme = True
        repo.create_head('main', origin.refs.psycho)
        repo.heads.psycho.set_tracking_branch(origin.refs.psycho)
        repo.heads.psycho.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'psycho':
        await ups.edit(
            f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). '
            'in that case, Updater is unable to identify '
             'which branch is to be merged. '
            'Please checkout the official branch`')
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_updateme:
        await ups.edit(
            f'Astro Is Using Lastest vision🌌\nI am Up-to-Dated with [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})😁')
        repo.__del__()
        return

    if conf != "now" and not force_updateme:
        changelog_str = f'**New UPDATE available for ASTRO🌌 [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):**\n\n' + '**CHANGES**\n\n' + f'{changelog}'
        if len(changelog_str) > 4095:
            await ups.edit("`Changes is too big, view the file to see it.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond(f'Do `.update now` to update')
        return

    if force_updateme:
        await ups.edit(
            'Force-Updating to latest stable code, please wait sir😁...')
    else:
        await ups.edit('__Updating your` 𝙰𝚜𝚝𝚛𝚘🌌 `please wait for a while_'_)
        await asyncio.sleep(4)
        await ups.edit('Updated 🌌Astro✨\nRestarting it please have patience and enjoy botless life for a while\n😁✌️ ')
        await borg.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    # You probably don't need it but whatever
    quit()
    # We're in a Heroku Dyno, handle it's memez.
    if Config.HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not Config.HEROKU_APP_NAME:
            await ups.edit('`Please set up the HEROKU_APP_NAME .`')
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == Config.HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f'{txt}\n`Invalid Heroku credentials for updating.`'
            )
            repo.__del__()
            return
        await ups.edit('Updating Started 😎😎✨\nRestarting, please wait 5min then type .alive to check if I alive!!!🙂\n Report Errors at @Astro_HelpChat'
                       )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Config.HEROKU_API_KEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/psycho", force=True)
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Here is the error log:\n{error}`')
            repo.__del__()
            return
        await ups.edit('`Sync Verified Successfully 🙂🙂\n'
                       'Restarting, please wait a min ,then type `.alive` to check if I alive')
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await ups.edit('`Successfully Updated!\n'
                      '𝙰𝚜𝚝𝚛𝚘 is restarting... Wait for a while then try .ping`')
        # Spin a new instance of bot
        args = [sys.executable, "-m", "astro"]
        execle(sys.executable, *args, environ)
        return