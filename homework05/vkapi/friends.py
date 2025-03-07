import dataclasses
import math
import time
import typing as tp
from tqdm import tqdm

from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    res = session.get(
        f"friends.get?access_token={config.VK_CONFIG['access_token']}&user_id={user_id}"
        f"&fields={','.join(fields) if fields else ''}&v={config.VK_CONFIG['version']}"
        f"&offset={offset}&count={count}"
    ).json()["response"]

    return FriendsResponse(**res)


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=tqdm,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    if target_uids:
        x = []
        y = int(len(target_uids) / 100) if int(len(target_uids) / 100) else 1
        for t in progress(range(y)):
            offset = 100 * t
            r = session.get(
                f"friends.getMutual?access_token={config.VK_CONFIG['access_token']}"
                f"&source_uid={source_uid if source_uid else ''}"
                f"&target_uids={','.join(map(str, target_uids)) if target_uids else ''}&order={order if order else ''}"
                f"&count={count if count else ''}&offset={offset if offset else 0}"
                f"&v={config.VK_CONFIG['version']}"
            ).json()
            try:
                data = r["response"]
            except KeyError:
                raise APIError(r["error"])
            x += [MutualFriends(**f) for f in data]  # type: ignore
            if t % 3 == 2:
                time.sleep(1)
        return x
    else:
        r = session.get(
            f"friends.getMutual?access_token={config.VK_CONFIG['access_token']}"
            f"&source_uid={source_uid if source_uid else ''}&target_uid={target_uid if target_uid else ''}"
            f"&order={order if order else ''}"
            f"&count={count if count else ''}&offset={offset if offset else 0}"
            f"&v={config.VK_CONFIG['version']}"
        ).json()
        try:
            return r["response"]
        except KeyError:
            raise APIError(r["error"])
