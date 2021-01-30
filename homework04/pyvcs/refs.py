import pathlib
import typing as tp


def update_ref(
    gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str
) -> None:
    # PUT YOUR CODE HERE
    with open((gitdir / ref), "w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / name, "w") as file:
        file.write("ref: " + ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if (gitdir / refname).exists():
        with open(gitdir / refname) as file:
            return file.read().strip()
    return None  # type: ignore


def resolve_head(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    HEAD = "HEAD"
    with open(gitdir / HEAD) as file:
        return len(file.read()) == 40


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    HEAD = "HEAD"
    with open(gitdir / HEAD) as file:
        return file.read().split()[1].strip()
