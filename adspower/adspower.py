import time
import requests

from typing import Dict, List, Optional

from .errors import (
    ProfileLimitReached,
    TooManyRequests,
    UnableToSetProxy,
    UnableToStartBrowser,
    UnableToStopBrowser,
    UnexpectedError,
)
from .models import Browser, GroupInfo, ProfileInfo, ProxyConfig, FingerprintConfig


class AdsPower:
    base_url: str
    group_url: str
    browser_url: str
    profile_url: str

    profiles: Dict[str, ProfileInfo]
    groups: Dict[str, GroupInfo]

    def __init__(self):
        self.base_url = "http://local.adspower.net:50325/api/v1"
        self.group_url = f"{self.base_url}/group"
        self.browser_url = f"{self.base_url}/browser"
        self.profile_url = f"{self.base_url}/user"

        self.profiles = None
        self.groups = None

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        resp = requests.request(method, url, **kwargs)
        time.sleep(1)

        json = resp.json()
        if json["code"] != 0:
            message = json["msg"].lower()
            if "many" in message:
                raise TooManyRequests()

            if "proxy fail" in message:
                raise UnableToSetProxy()

            if "accounts exceeds" in message:
                raise ProfileLimitReached()

            if "account does not exist" in message:
                raise UnableToStartBrowser()

            if "is not open" in message:
                raise UnableToStopBrowser()

            raise UnexpectedError(json)

        return resp

    def create_profile(
        self,
        group_id: str,
        user_proxy_config: ProxyConfig,
        fingerprint_config: FingerprintConfig,
        name="",
        domain_name: Optional[str] = "",
        open_urls: Optional[List[str]] = [],
        repeat_config: Optional[str] = "",
        username: Optional[str] = "",
        password: Optional[str] = "",
        fakey: Optional[str] = "",
        cookie: Optional[str] = "",
        ignore_cookie_error: Optional[str] = "",
        ip: Optional[str] = "",
        country: Optional[str] = "",
        region: Optional[str] = "",
        city: Optional[str] = "",
        remark: Optional[str] = "",
        ipchecker: Optional[str] = "",
        sys_app_cate_id: Optional[str] = "",
    ) -> str:
        """
        More info can be found via url:
        https://localapi-doc-en.adspower.com/docs/XDhI2D
        """
        url = f"{self.profile_url}/create"

        payload = {
            "group_id": group_id,
            "user_proxy_config": user_proxy_config.to_json(),
            "fingerprint_config": fingerprint_config.to_json(),
        }

        if name != "":
            payload["name"] = name

        if domain_name != "":
            payload["domain_name"] = domain_name

        if len(open_urls) != 0:
            payload["open_urls"] = open_urls

        if repeat_config != "":
            payload["repeat_config"] = repeat_config

        if username != "":
            payload["username"] = username

        if password != "":
            payload["password"] = password

        if fakey != "":
            payload["fakey"] = fakey

        if cookie != "":
            payload["cookie"] = cookie

        if ignore_cookie_error != "":
            payload["ignore_cookie_error"] = ignore_cookie_error

        if ip != "":
            payload["ip"] = ip

        if country != "":
            payload["country"] = country

        if region != "":
            payload["region"] = region

        if city != "":
            payload["city"] = city

        if remark != "":
            payload["remark"] = remark

        if ipchecker != "":
            payload["ipchecker"] = ipchecker

        if sys_app_cate_id != "":
            payload["sys_app_cate_id"] = sys_app_cate_id

        resp = self._request("POST", url, json=payload)
        json = resp.json()

        user_id = json["data"]["id"]
        return user_id

    def create_profile_if_not_exists(
        self,
        name: str,
        group_id: str,
        user_proxy_config: ProxyConfig,
        fingerprint_config: FingerprintConfig,
        domain_name: Optional[str] = "",
        open_urls: Optional[List[str]] = [],
        repeat_config: Optional[str] = "",
        username: Optional[str] = "",
        password: Optional[str] = "",
        fakey: Optional[str] = "",
        cookie: Optional[str] = "",
        ignore_cookie_error: Optional[str] = "",
        ip: Optional[str] = "",
        country: Optional[str] = "",
        region: Optional[str] = "",
        city: Optional[str] = "",
        remark: Optional[str] = "",
        ipchecker: Optional[str] = "",
        sys_app_cate_id: Optional[str] = "",
    ) -> bool:
        profile_info = self.query_profile_info_by_name(name)
        if not profile_info:
            return self.create_profile(
                group_id,
                user_proxy_config,
                fingerprint_config,
                name,
                domain_name,
                open_urls,
                repeat_config,
                username,
                password,
                fakey,
                cookie,
                ignore_cookie_error,
                ip,
                country,
                region,
                city,
                remark,
                ipchecker,
                sys_app_cate_id,
            )

        return False

    def update_profile(
        self,
        user_id: str,
        name: Optional[str] = "",
        domain_name: Optional[str] = "",
        open_urls: Optional[List[str]] = [],
        repeat_config: Optional[str] = "",
        username: Optional[str] = "",
        password: Optional[str] = "",
        fakey: Optional[str] = "",
        cookie: Optional[str] = "",
        ignore_cookie_error: Optional[str] = "",
        ip: Optional[str] = "",
        country: Optional[str] = "",
        region: Optional[str] = "",
        city: Optional[str] = "",
        remark: Optional[str] = "",
        ipchecker: Optional[str] = "",
        sys_app_cate_id: Optional[str] = "",
        user_proxy_config: ProxyConfig = None,
        fingerprint_config: FingerprintConfig = None,
    ):
        """
        More info can be found via url:
        https://localapi-doc-en.adspower.com/docs/XDhI2D
        """

        url = f"{self.profile_url}/update"
        payload = {"user_id": user_id}

        if name != "":
            payload["name"] = name

        if domain_name != "":
            payload["domain_name"] = domain_name

        if len(open_urls) != 0:
            payload["open_urls"] = open_urls

        if repeat_config != "":
            payload["repeat_config"] = repeat_config

        if username != "":
            payload["username"] = username

        if password != "":
            payload["password"] = password

        if fakey != "":
            payload["fakey"] = fakey

        if cookie != "":
            payload["cookie"] = cookie

        if ignore_cookie_error != "":
            payload["ignore_cookie_error"] = ignore_cookie_error

        if ip != "":
            payload["ip"] = ip

        if country != "":
            payload["country"] = country

        if region != "":
            payload["region"] = region

        if city != "":
            payload["city"] = city

        if remark != "":
            payload["remark"] = remark

        if ipchecker != "":
            payload["ipchecker"] = ipchecker

        if sys_app_cate_id != "":
            payload["sys_app_cate_id"] = sys_app_cate_id

        if user_proxy_config != None:
            payload["user_proxy_config"] = user_proxy_config.json()

        if fingerprint_config != None:
            payload["fingerprint_config"] = fingerprint_config.json()

        self._request("POST", url, json=payload)
        return True

    def update_profile_by_name(
        self,
        name: str,
        domain_name: Optional[str] = "",
        open_urls: Optional[List[str]] = [],
        repeat_config: Optional[str] = "",
        username: Optional[str] = "",
        password: Optional[str] = "",
        fakey: Optional[str] = "",
        cookie: Optional[str] = "",
        ignore_cookie_error: Optional[str] = "",
        ip: Optional[str] = "",
        country: Optional[str] = "",
        region: Optional[str] = "",
        city: Optional[str] = "",
        remark: Optional[str] = "",
        ipchecker: Optional[str] = "",
        sys_app_cate_id: Optional[str] = "",
        user_proxy_config: ProxyConfig = None,
        fingerprint_config: FingerprintConfig = None,
        refresh: bool = False,
    ):
        profile_info = self.query_profile_info_by_name(name, refresh=refresh)
        if not profile_info:
            return None

        self.update_profile(
            profile_info.user_id,
            name,
            domain_name,
            open_urls,
            repeat_config,
            username,
            password,
            fakey,
            cookie,
            ignore_cookie_error,
            ip,
            country,
            region,
            city,
            remark,
            ipchecker,
            sys_app_cate_id,
            user_proxy_config,
            fingerprint_config,
        )

        return True

    def check_browser_status(self, user_id: str) -> Browser | None:
        profile_info = self.query_profiles_info(user_id=user_id)
        if not profile_info:
            return None

        url = f"{self.browser_url}/active?user_id={user_id}"

        resp = self._request("GET", url)
        json = resp.json()

        return Browser(json)

    def start_browser(self, user_id: str, ip_tab: str = "") -> Browser:
        """
        More info can be found via url:
        https://localapi-doc-en.adspower.com/docs/FFMFMf
        """

        url = f"{self.browser_url}/start?user_id={user_id}"

        if ip_tab != "":
            url = f"{url}&ip_tab={ip_tab}"

        resp = self._request("GET", url)
        json = resp.json()

        return Browser.from_json(json) 

    def stop_browser(self, user_id: str) -> bool:
        """
        More info can be found via url:
        https://localapi-doc-en.adspower.com/docs/DXam94
        """

        url = f"{self.browser_url}/stop?user_id={user_id}"

        self._request("GET", url)
        return True

    def query_profiles_info(
        self,
        group_id="",
        user_id="",
        serial_number="",
        limit: int = 100,
        offcet: int = 1,
        refresh: bool = False,
    ) -> Dict[str, ProfileInfo] | None:
        """
        More info can be found via url:
        https://localapi-doc-en.adspower.com/docs/u8m2Ie
        """

        url = f"{self.profile_url}/list?page={offcet}&page_size={limit}"

        if not refresh:
            profiles = self.profiles
            if profiles:
                return profiles

        if group_id != "":
            url = f"{url}&group_id={group_id}"

        if user_id != "":
            url = f"{url}&&user_id={user_id}"

        if serial_number != "":
            url = f"{url}&serial_number={serial_number}"

        resp = self._request("GET", url)
        json = resp.json()

        data = json["data"]
        if len(data["list"]) == 0:
            return None

        raw_profiles = json["data"]["list"]
        profiles = {}
        for raw_profile in raw_profiles:
            profile_name = raw_profile["name"]
            profile_info = ProfileInfo(raw_profile)
            profiles[profile_name] = profile_info

        self.profiles = profiles
        return profiles

    def query_profile_info_by_name(
        self, name: str, refresh: bool = False
    ) -> ProfileInfo | None:
        profiles = self.query_profiles_info(refresh=refresh)
        if not profile:
            return None
        
        try:
            profile = profiles[name]
        except KeyError:
            return None

        return profile

    def query_groups_info(
        self,
        group_name: str = "",
        offcet: int = 1,
        limit: int = 2000,
        refresh: bool = False,
    ) -> Dict[str, GroupInfo] | GroupInfo:
        if not refresh:
            groups = self.groups
            if groups:
                return groups

        url = f"{self.group_url}/list?page={offcet}&page_size={limit}"

        if group_name != "":
            url = f"{url}&group_name={group_name}"

        resp = self._request("GET", url)
        json = resp.json()

        raw_groups = json["data"]["list"]
        groups = {}
        for raw_group in raw_groups:
            group_name = raw_group["group_name"]
            group_info = GroupInfo(raw_group)
            groups[group_name] = group_info

        self.groups = groups
        return groups

    def query_group_info(
        self, group_name: str, refresh: bool = False
    ) -> GroupInfo | None:
        groups_info = self.query_groups_info(
            group_name, offcet=1, limit=1, refresh=refresh
        )
        return groups_info[group_name] if len(groups_info) == 1 else None
