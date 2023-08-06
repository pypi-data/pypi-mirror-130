from abc import ABC


class apifx(ABC):
    """FaaS API function Class

    Returns:
        Class: FaaS API Function
    """

    # "http://{server}:{port}/function/{fx}.faas-{type}-fn"
    _url: str
    def __init__(self, url: str = None) -> None:
        """init

        Args:
            url (str, optional): url of FaaS functions. Defaults to None.
        """
        self._url = url
        pass
    def get(self, fx: str, data: dict, type: str = "pri", isjson: bool = True) -> list:
        """get function

        Args:
            fx (str): func name
            data (dict): data body
            type (str, optional): env - pub / pri. Defaults to "pri".
            isjson (bool, optional): True - convert to json / False. Defaults to True.

        Returns:
            list: [description]
        """
        import requests
        import json
        _url = self._url.format(fx, type)
        _data = json.dumps(data)
        rtn = requests.get(_url, data=_data)
        if rtn.status_code!=200:
            return [rtn.text]
        rtn.encoding = 'utf-8'
        if isjson:
            _rjson = rtn.json()
            if _rjson.get("code", 404)!=200:
                return [_rjson]
            return _rjson.get("data", [])
        else:
            return rtn.text
