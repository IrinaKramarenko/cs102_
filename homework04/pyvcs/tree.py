import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content: tp.List[tp.Tuple[int, str, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    files = []
    for x in (gitdir.parent / dirname).glob("*"):
        files.append(str(x))
    for entry in index:
        if entry.name in files:
            tree_content.append((entry.mode, str(gitdir.parent / entry.name), entry.sha1))
        else:
            dname = entry.name.lstrip(dirname).split("/", 1)[0]
            if not dname in subtrees:
                subtrees[dname] = []
            subtrees[dname].append(entry)
    for name in subtrees:
        if dirname != "":
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], dirname + "/" + name)),
                )
            )
        else:
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], name)),
                )
            )
    tree_content.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2] for elem in tree_content
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    now = int(time.mktime(time.localtime()))
    timezone = time.timezone
    if timezone > 0:
        formatted_timezone = "-"
    else:
        formatted_timezone = "+"
    formatted_timezone += f"{abs(timezone) // 3600:02}{abs(timezone) // 60 % 60:02}"
    commit_content = []
    commit_content.append(f"tree {tree}")
    if parent is not None:
        commit_content.append(f"parent {parent}")
    commit_content.append(f"author {author} {now} {formatted_timezone}")
    commit_content.append(f"committer {author} {now} {formatted_timezone}")
    commit_content.append(f"\n{message}\n")
    data = "\n".join(commit_content).encode()
    return hash_object(data, "commit", write=True)
