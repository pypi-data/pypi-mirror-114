# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from portmod.repo import get_repo
from portmod.repos import add_repo, get_local_repos
from portmod.sync import sync
from portmodlib.l10n import l10n

from .select import get_repos_list


def sync_args(args):
    local_repos = get_local_repos()
    remote_repos = get_repos_list()
    if args.repository:
        to_sync = []
        for name in args.repository:
            repo = add_repo(next(repo for repo in remote_repos if repo.name == name))
            if repo:
                to_sync.append(repo)
            else:
                to_sync.append(local_repos[name])
        sync([get_repo(name) for name in args.repository])
    else:
        sync(local_repos.values())


def add_sync_parser(subparsers, parents):
    parser = subparsers.add_parser("sync", help=l10n("sync-help"), parents=parents)
    parser.add_argument(
        "repository",
        help=l10n("sync-repositories-help"),
        nargs="*",
    )
    parser.set_defaults(func=sync_args)
