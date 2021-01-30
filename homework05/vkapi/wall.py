# import textwrap
import time
import typing as tp

import pandas as pd  # type: ignore

from tqdm import tqdm  # type: ignore

from vkapi import config, session  # type: ignore
from vkapi.exceptions import APIError  # type: ignore


class Params(tp.TypedDict):
    owner_id: str
    domain: str
    offset: int
    count: int
    filter: str
    extended: int
    fields: str
    max_count: int


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> Params:
    params_: Params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": count,
        "filter": filter,
        "extended": extended,
        "fields": ",".join(fields) if fields else "",
        "max_count": max_count,
    }
    return params_


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 100,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=tqdm,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    params_: Params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": count,
        "filter": filter,
        "extended": extended,
        "fields": ",".join(fields) if fields else "",
        "max_count": max_count,
    }

    code = (
        """
        var calls = 0,
            items = [],
            records = 0,
            params = """
        + str(params_)
        + """,
        response = {"count":"1"};

    if (params.count == 0){
        params.count = 100;
        response = API.wall.get(params);
        records = response.count;
        items = items + response.items;
        calls = calls + 1;
    }else{
        records = params.count;
        if (params.count >= 100){
            params.count = 100;
        }        
    }
    var max_calls = """
        + str(max_count)
        + """ / 100; 
    while(calls < max_calls && records > params.offset) {

        calls = calls + 1;  

        response = API.wall.get(params);
        items = items + response.items;
        params.offset = params.offset + params.count;
    };
    return {
        count: records,
        items: items
     };"""
    )

    params = {
        "code": code,
        "access_token": config.VK_CONFIG["access_token"],
        "v": "5.126",
        "count": 0,
    }

    class Response(tp.TypedDict):
        items: list
        count: int

    res: Response = {"items": [], "count": 1}

    with progress(total=res["count"]) as pbar:
        while len(res["items"]) < res["count"]:
            j = session.post(url="execute", data=params).json()

            time.sleep(1)

            try:
                if j["response"]["items"]:
                    res["items"] += j["response"]["items"]
                else:
                    res["items"] += [
                        i
                        for i in range(
                            2500
                            if res["count"] - len(res["items"]) > 2500
                            else res["count"] - len(res["items"])
                        )
                    ]
                res["count"] = j["response"]["count"]
            except KeyError:
                raise APIError(j["error"])

            params["count"] = int(res["count"])
            pbar.total = res["count"]
            pbar.update(len(res["items"]) - params_["offset"])
            params_["offset"] = len(res["items"])

    return pd.DataFrame(res["items"])
