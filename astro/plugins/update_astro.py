# Astro-UB
import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from astro import CMD_HNDLR

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)

HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
GIT_REPO_NAME = "Astro-UB"
UPSTREAM_REPO_URL = "https://github.com/PsychoBots/Astro-UB"

xxxx = CMD_HNDLR if CMD_HNDLR else "."


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On " + "%d/%m/%y" + " at " + "%H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by **{c.author}**\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@astro.on(admin_cmd(pattern="update ?(.*)"))
async def upstream(ups):
    await ups.edit("Searching for new updates, if any..🤷")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_updateme = False

    try:
        txt = "`Oops.. Updater cannot continue as🥺🥺🥺"
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await ups.edit(
                f"Ohh Yeah...👀\n\nYour **Astro Has Got Some Update use** .update now to update"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_updateme = True
        repo.create_head("psycho", origin.refs.psycho)
        repo.heads.psycho.set_tracking_branch(origin.refs.psycho)
        repo.heads.psycho.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != "psycho":
        await ups.edit(
            f"**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "Please checkout the official branch of astro`"
        )
        repo.__del__()
        return

    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if not changelog and not force_updateme:
        await ups.edit(
            f"\n**Astro is using Latest vision**[[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})\nYou Have Up-to-dated Branch😁"
        )
        repo.__del__()
        return

    if conf != "now" and not force_updateme:
        changelog_str = (
            f"**New UPDATE available for [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):**\n\n"
            + "**CHANGES**\n\n"
            + f"{changelog}"
        )
        if len(changelog_str) > 4096:
            await ups.edit("`ChangeS is too big, view the file to see it.`")
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
        await ups.respond(f"Do `{xxxx}update now` to update")
        return

    if force_updateme:
        await ups.edit("`Force-Syncing to latest stable userbot code, please wait...`")
    else:
        await ups.edit("`Starting Updater Of Astro...\nPlease wait....`")
    # We're in a Heroku Dyno, handle it's memez.
    if Config.HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not Config.HEROKU_APP_NAME:
            await ups.edit(
                "`Please set up the HEROKU_APP_NAME Configiable to be able to update userbot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == Config.HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f"{txt}\n`Invalid Heroku credentials for updating userbot dyno.`"
            )
            repo.__del__()
            return
        await ups.edit(
            "Astro dyno build in progress, please wait for it to complete.")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◘◘◘◘◘◘◘◘0%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◘◘◘◘◘◘20%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◘◘◘◘◘39%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◙◘◘◘◘50%")
        await ups.edit("Update..in progress\n◙◙◙◙◙◘◘◘68%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◙◙◙◘◘75%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◙◙◙◘◘80%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◙◙◙◙◘90%")
        await asyncio.sleep(1)
        await ups.edit("Update..in progress\n◙◙◙◙◙◙◙◙100%")
        await asyncio.sleep(1)
        await ups.edit("__Your ƛsτʀ๏ is Updated Sucessfully🤗__\nPlease wait 5min. to re-Start\nuntil a New Deploy Message is Dropped in your Private group")
        
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Config.HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/psycho", force=True)
        except GitCommandError as error:
            await ups.edit(f"{txt}\n`Here is the error log:\n{error}`")
            repo.__del__()
            return
        await ups.edit("Successfully Updated!\n" "Restarting, please wait...")
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await ups.edit(
            "`Successfully Updated!\n" "Bot is restarting... Wait for a second!`"
        )
        # Spin a new instance of bot
        args = [sys.executable, "-m", "astro"]
        execle(sys.executable, *args, environ)
        return
