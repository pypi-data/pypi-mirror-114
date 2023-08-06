# coding=utf-8
"""
Common shared functions and classes
"""
from json import dumps, loads
from typing import Any, Dict, Optional

import aiohttp
import shortuuid


async def getsecret(sname: str, fid: str, atoken: str) -> Optional[str]:
    """
    Returns the secret value from Yandex Cloud Lockbox

    :param sname: name of a secret
    :param fid: folderId of the cloud folder
    :param atoken: access token for Lockbox API
    :return: secret contents
    """
    async with aiohttp.ClientSession(raise_for_status=True) as s:
        async with s.get(f"https://lockbox.api.cloud.yandex.net/lockbox/v1/secrets?folderId={fid}",
                         headers={"Authorization": f"Bearer {atoken}"}) as r:
            _list = await r.json()
            for _s_item in _list["secrets"]:
                if _s_item["name"] == sname:
                    _sid = _s_item["id"]
                    async with s.get(f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{_sid}/payload",
                                     headers={"Authorization": f"Bearer {atoken}"}) as nr:
                        _secret = await nr.json()
                        return _secret["entries"][0]["textValue"]
    return None


async def tgmjsoncall(tgs: aiohttp.client.ClientSession,
                      tgmethod: str,
                      tgtoken: str,
                      tgjson: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call the Telegram Bot API method with application/json formatted payload

    :param tgs: aiohttp session to use
    :param tgmethod:  method name
    :param tgtoken: bot token string
    :param tgjson: dict object with JSON to send to the Bot API
    :return: method result received from Telegram Bot API deserialized into dict with loads()
    """
    async with tgs.post(f"https://api.telegram.org/bot{tgtoken}/{tgmethod}",
                        headers={"Content-Type": "application/json"},
                        data=dumps(tgjson, ensure_ascii=False),
                        raise_for_status=False) as r:
        _tgm_response = await r.json()
        # Check the received response
        if "ok" in _tgm_response.keys():
            if _tgm_response["ok"]:
                # This means method sent OK
                return _tgm_response["result"]
            else:
                raise RuntimeError(f"Telegram Bot API {tgmethod} call error: "
                                   f"{dumps(_tgm_response)}")
        else:
            raise RuntimeError(f"Telegram Bot API wrong response: {dumps(_tgm_response)}")


class WorkItem:
    """
    Main object that Telegram Bot works with - the work item, represents task to do
    """

    def __init__(self, jsonsrc: Optional[str] = None):
        """
        Instantiate the object from JSON string, or by default create empty object

        :param jsonsrc: optional JSON representation of WorkItemIssue
        """
        if jsonsrc is not None and isinstance(jsonsrc, (str, bytes,)):
            _j = loads(jsonsrc)
        else:
            _j = dict()
        self._wi = {"id":         _j["id"] if "id" in _j.keys() and isinstance(_j["id"],
                                                                               (str, bytes,)) else shortuuid.uuid(),
                    "chat_id":    _j["chat_id"] if "chat_id" in _j.keys() and isinstance(_j["chat_id"], int) else None,
                    "logbook_id": _j["logbook_id"] if "logbook_id" in _j.keys() and isinstance(_j["logbook_id"],
                                                                                               int) else None,
                    "domain":     _j["domain"] if "domain" in _j.keys() and isinstance(_j["domain"], str) else None,
                    "site_id":    _j["site_id"] if "site_id" in _j.keys() and isinstance(_j["site_id"], int) else None,
                    "type_id":    _j["type_id"] if "type_id" in _j.keys() and isinstance(_j["type_id"], int) else None,
                    "text":       _j["text"] if "text" in _j.keys() and isinstance(_j["text"], str) else None,
                    "title":      _j["title"] if "title" in _j.keys() and isinstance(_j["title"], str) else None,
                    "desc":       _j["desc"] if "desc" in _j.keys() and isinstance(_j["desc"], str) else None,
                    "photo":      _j["photo"] if "photo" in _j.keys() and isinstance(_j["photo"], bool) else False,
                    "photo_path": _j["photo_path"] if "photo_path" in _j.keys() and isinstance(_j["photo_path"],
                                                                                               str) else None,
                    "photo_s3":   _j["photo_s3"] if "photo_s3" in _j.keys() and isinstance(_j["photo_s3"],
                                                                                           str) else None,
                    "voice":      _j["voice"] if "voice" in _j.keys() and isinstance(_j["voice"], bool) else False,
                    "voice_len":  _j["voice_len"] if "voice_len" in _j.keys() and isinstance(_j["voice_len"],
                                                                                             int) else False,
                    "voice_path": _j["voice_path"] if "voice_path" in _j.keys() and isinstance(_j["voice_path"],
                                                                                               str) else None,
                    "voice_s3":   _j["voice_s3"] if "voice_s3" in _j.keys() and isinstance(_j["voice_s3"],
                                                                                           str) else None,
                    "state":      _j["state"] if "state" in _j.keys() and isinstance(_j["state"], str) else None,
                    "assign_id":  _j["assign_id"] if "assign_id" in _j.keys() and isinstance(_j["assign_id"],
                                                                                             int) else None
                    }

    def __str__(self) -> str:
        """
        Get the JSON string representation

        :return: JSON serialized
        """
        return dumps(self._wi, ensure_ascii=False)

    def set(self, k: str, v: Any) -> None:
        """
        Set the parameter

        :param k: parameter key
        :param v: value to set
        :return: nothing
        """
        self._wi[k] = v

    def get(self, k: str) -> Any:
        """
        Get the parameter value

        :param k: parameter key
        :return: value of parameter
        """
        return self._wi[k]
