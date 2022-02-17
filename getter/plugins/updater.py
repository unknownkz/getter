# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

from asyncio import Lock, sleep
from contextlib import suppress
from os import execl
from random import randrange
from sys import executable
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from heroku3 import from_key
from . import (
    DEVS,
    HELP,
    Root,
    Var,
    __version__,
    eor,
    eod,
    hl,
    kasta_cmd,
    runner,
)

UPDATE_LOCK = Lock()
requirements = Root / "requirements.txt"
off_repo = "https://github.com/kastaid/getter"
help_text = f"""
`{hl}update <now|pull|one>` for temporary update as locally.
`{hl}update <deploy|push|all>` for permanently update as heroku.
"""


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y || %H:%M"
    return "".join(
        f" • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n" for c in repo.iter_commits(diff)
    )


async def print_changelogs(Kst, ac_br, changelog):
    text = f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    file = "changelog_output.txt"
    if len(text) > 4096:
        await Kst.edit("View the file to see it.")
        with open(file, "w+") as f:
            f.write(text)
        await Kst.reply(file=file, silent=True)
        (Root / file).unlink(missing_ok=True)
    else:
        await Kst.edit(text)


async def pulling(Kst, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await runner("pip3 install --no-cache-dir -r requirements.txt")
    await eod(Kst, "`[PULL] Update Successfully, Rebooting... Wait for a minute!`")
    execl(executable, executable, "-m", "getter")
    return


async def pushing(Kst, repo, ups_rem, ac_br, txt):
    if not (Var.HEROKU_API and Var.HEROKU_APP_NAME):
        await eod(Kst, "Please set `HEROKU_APP_NAME` and `HEROKU_API` in vars.")
        return
    heroku = from_key(Var.HEROKU_API)
    heroku_app = None
    heroku_applications = heroku.apps()
    for app in heroku_applications:
        if app.name == Var.HEROKU_APP_NAME:
            heroku_app = app
            break
    if not heroku_app:
        await eod(Kst, f"{txt}\n`Invalid Heroku credentials for deploying app.`")
        repo.__del__()
        return
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace("https://", "https://api:" + Var.HEROKU_API + "@")
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    with suppress(BaseException):
        remote.push(refspec="HEAD:refs/heads/main", force=True)
    build = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build.status == "failed":
        await eod(Kst, "`Deploy failed, detected some errors...`")
        return
    await eod(Kst, "`[PUSH] Update Successfully, Rebooting... Wait for a minute!`")
    return


@kasta_cmd(pattern="update(?: |$)(now|deploy|pull|push|one|all)?(?: |$)(.*)")
@kasta_cmd(own=True, senders=DEVS, pattern="getterup(?: |$)(now|deploy|pull|push|one|all)?(?: |$)(.*)")
async def _(e):
    is_devs = True if not (hasattr(e, "out") and e.out) else False
    if is_devs and e.client.uid in DEVS:
        return
    if UPDATE_LOCK.locked():
        await eod(e, "`Please wait until previous UPDATE finished !!`", time=5, silent=True)
        return
    async with UPDATE_LOCK:
        mode = e.pattern_match.group(1)
        opt = e.pattern_match.group(2)
        force_update = is_deploy = is_now = False
        if mode in ["deploy", "push", "all"]:
            is_deploy = True
        if mode in ["now", "pull", "one"]:
            is_now = True
        if is_devs and opt:
            user_id = version = None
            try:
                user_id = int(opt)
            except ValueError:
                version = opt
            if not version and user_id != e.client.uid:
                return
            if not user_id and version == __version__:
                return
        Kst = await eor(e, "`Fetching...`", silent=True)
        if is_devs:
            await sleep(randrange(2, 4))
        """
        if is_deploy:
            with suppress(BaseException):
                from os import chdir
                chdir("/app")
                await runner("rm -rf .git")
        """
        try:
            txt = "**Oops... Updater cannot continue due to some problems occured.**\n"
            repo = Repo()
        except NoSuchPathError as err:
            await Kst.edit(f"{txt}\n`directory {err} is not found`")
            Repo().__del__()
            return
        except GitCommandError as err:
            await Kst.edit(f"{txt}\n`Early failure! {err}`")
            Repo().__del__()
            return
        except InvalidGitRepositoryError:
            repo = Repo.init()
            origin = repo.create_remote("upstream", off_repo)
            origin.fetch()
            if is_now:
                force_update = True
            repo.create_head("main", origin.refs.main)
            repo.heads.main.set_tracking_branch(origin.refs.main)
            repo.heads.main.checkout(True)
        ac_br = repo.active_branch.name
        with suppress(BaseException):
            repo.create_remote("upstream", off_repo)
        ups_rem = repo.remote("upstream")
        ups_rem.fetch(ac_br)
        if is_deploy:
            if is_devs:
                await sleep(randrange(4, 6))
            await Kst.edit("`Deploying, please wait...`")
            await pushing(Kst, repo, ups_rem, ac_br, txt)
            return
        changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
        if changelog == "" and not force_update:
            await eor(Kst, f"v{__version__} **up-to-date** as `main`", time=15)
            repo.__del__()
            return
        if mode == "" and not force_update:
            await print_changelogs(Kst, ac_br, changelog)
            await Kst.reply(help_text, silent=True)
            return
        if force_update:
            await Kst.edit("`Force-Syncing to latest source code, please wait...`")
        else:
            await Kst.edit("`Updating, plase wait...`")
        if is_now:
            await pulling(Kst, repo, ups_rem, ac_br)
        return


@kasta_cmd(pattern="repo$")
async def _(e):
    await e.eor(
        f"""
• **Repo**: [GitHub](https://github.com/kastaid/getter)
• **Deploy**: [View at @kastaid](https://t.me/kastaid/9)
""",
    )


HELP.update(
    {
        "updater": [
            "Updater",
            """• `{i}update`
↳ : Checks for updates, also displaying the changelog.

• `{i}update <now|pull|one>`
↳ : Temporary update as locally if available from repo.

• `{i}update <deploy|push|all>`
↳ : Permanently update as heroku, will forced deploy.

• `{i}repo`
↳ : Get repo link.
""",
        ]
    }
)
