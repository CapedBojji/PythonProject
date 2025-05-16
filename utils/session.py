import http.cookies
import logging

import requests
from requests.cookies import RequestsCookieJar, create_cookie


def create_session(selenium_cookie_list: list[dict]) -> requests.Session:
    """
    Create a requests session with the given cookies.

    :param selenium_cookie_list : list[dict]
            - A list of dictionaries, each representing a cookie;
            - With required keys - "name" and "value";
            - Optional keys - "path", "domain", "secure", "httpOnly", "expiry", "sameSite"
    :return: A requests session with the cookies set.
    """
    session = requests.Session()
    for cookie in selenium_cookie_list:
        fixed_cookie = {**{k: v for k, v, in cookie.items() if k not in ("expiry", "sameSite", "httpOnly")}}
        if cookie.get("expiry"):
            fixed_cookie["expires"] = cookie["expiry"]
        session.cookies.set_cookie(create_cookie(**fixed_cookie))
    return session

def log_response_error(response: requests.Response, message: str, *args) -> bool:
    """
    Log the error response.

    :param response: The response object.
    """
    if response.status_code != 200:
        logging.error(message, *args)
        return True
    return False
