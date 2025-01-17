# getter < https://t.me/kastaid >
# Copyright (C) 2022 - kastaid
# All rights reserved.
#
# This file is a part of < https://github.com/kastaid/getter/ >
# PLease read the GNU Affero General Public License in;
# < https://www.github.com/kastaid/getter/blob/main/LICENSE/ >
# ================================================================

import sys
from asyncio import Lock, sleep
from contextlib import suppress
from os import close, execl, getpid
from secrets import choice
import psutil as psu
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from heroku3 import from_key
from . import (
    __version__,
    Root,
    HELP,
    DEVS,
    Var,
    eor,
    eod,
    hl,
    kasta_cmd,
    Runner,
)

UPDATE_LOCK = Lock()
off_repo = "https://github.com/kastaid/getter.git"
help_text = f"""❯ `{hl}update <now|pull|one> <force|f>`
Temporary update as locally if available from repo.

❯ `{hl}update <deploy|push|all>`
Permanently update as heroku, will forced deploy.
"""


def gen_chlog(repo, diff):
    _ = off_repo.replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    ch = f"<b>Getter v{__version__} updates for <a href={_}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    d_form = "%d/%m/%Y %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={_.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
    if ch_log:
        return str(ch + ch_log)
    return ch_log


async def print_changelogs(e, changelog):
    file = "changelog_output.txt"
    if len(changelog) > 4096:
        await e.edit("View the file to see it.")
        with open(file, "w+") as f:
            f.write(changelog)
        await e.reply(file=file, silent=True)
        (Root / file).unlink(missing_ok=True)
    else:
        await e.edit(changelog, parse_mode="html")


async def pulling(e):
    await Runner("git pull -f && pip3 install --no-cache-dir -U -r requirements.txt")
    _ = f"`[PULL] Update Successfully...`\nWait for a few seconds, then run `{hl}ping` command."
    await eod(e, _)
    with suppress(psu.NoSuchProcess, psu.AccessDenied, psu.ZombieProcess):
        c_p = psu.Process(getpid())
        [close(h.fd) for h in c_p.open_files() + c_p.connections()]
    execl(sys.executable, sys.executable, "-m", "getter")
    return


async def pushing(e, repo, ups_rem, ac_br):
    if not Var.HEROKU_API:
        await eod(e, "Please set `HEROKU_API` in Config Vars.")
        return repo.__del__()
    if not Var.HEROKU_APP_NAME:
        await eod(e, "Please set `HEROKU_APP_NAME` in Config Vars.")
        return repo.__del__()
    heroku = from_key(Var.HEROKU_API)
    try:
        heroku_app = heroku.apps()[Var.HEROKU_APP_NAME]
    except KeyError:
        await eod(e, f"`HEROKU_APP_NAME config is invalid! Make sure an app with that name exists.`")
        return repo.__del__()
    except Exception as err:
        await eod(e, f"**Updating Deploy error:**\n```{err}```")
        return repo.__del__()
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_remote_url = heroku_app.git_url.replace("https://", f"https://api:{Var.HEROKU_API}@")
    remote = None
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_remote_url)
    else:
        remote = repo.create_remote("heroku", heroku_remote_url)
    with suppress(BaseException):
        remote.push(refspec="HEAD:refs/heads/main", force=True)
    build = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build.status == "failed":
        await eod(e, "`Build Deploy failed, detected some errors...`")
        return
    _ = f"`[PUSH] Update Successfully...`\nWait for a few minutes, then run `{hl}ping` command."
    await eod(e, _)


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
        is_deploy = is_now = force_now = False
        if mode in ["deploy", "push", "all"]:
            is_deploy = True
        if mode in ["now", "pull", "one"]:
            is_now = True
        if not Var.DEV_MODE and is_now and opt in ["force", "f"]:
            force_now = True
        if is_devs and opt and not force_now:
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
            await sleep(choice((2, 3, 4)))
        try:
            repo = Repo()
        except NoSuchPathError as err:
            await Kst.edit(f"`Directory {err} is not found`")
            return Repo().__del__()
        except GitCommandError as err:
            await Kst.edit(f"`Early failure! {err}`")
            return Repo().__del__()
        except InvalidGitRepositoryError:
            repo = Repo.init()
            origin = repo.create_remote("upstream", off_repo)
            origin.fetch()
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
                await sleep(choice((4, 5, 6)))
            await Kst.edit("`[PUSHING] Please wait...`")
            await pushing(Kst, repo, ups_rem, ac_br)
            return
        changelog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
        if not changelog and not force_now:
            await eod(Kst, f"`Getter v{__version__}` **up-to-date** [`{ac_br}`]", time=15)
            return repo.__del__()
        if not mode and not force_now:
            await print_changelogs(Kst, changelog)
            await Kst.reply(help_text, silent=True)
            return
        if force_now:
            await Kst.edit("`Force-Syncing to latest stable source code, please wait...`")
            await sleep(2)
        if is_now:
            await Kst.edit("`[PULLING] Plase wait...`")
            await pulling(Kst)
        return


@kasta_cmd(pattern="repo$")
async def _(e):
    await e.eor(
        """
• **Repo:** [GitHub](https://kasta.vercel.app/getter_source)
• **Deploy:** [View at @kastaid](https://kasta.vercel.app/getter_deploy)
""",
    )


HELP.update(
    {
        "updater": [
            "Updater",
            """❯ `{i}update`
Checks for updates, also displaying the changelog.

❯ `{i}update <now|pull|one> <force|f>`
Temporary update as locally if available from repo.

❯ `{i}update <deploy|push|all>`
Permanently update as heroku, will forced deploy.

❯ `{i}repo`
Get repo link.
""",
        ]
    }
)
