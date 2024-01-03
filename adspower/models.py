from dataclasses import dataclass
from typing import Dict, Optional, List
from urllib.parse import urlparse


@dataclass
class ProfileInfo:
    """
    More info can be found via url:
    https://localapi-doc-en.adspower.com/docs/u8m2Ie
    """

    serial_number: str
    domain_name: str
    ip: str
    ip_country: str
    username: str
    password: str
    fbcc_proxy_acc_id: str
    ipchecker: str
    fakey: str
    sys_app_cate_id: int
    group_id: str
    group_name: str
    remark: str
    created_time: int
    last_open_time: str
    user_id: str

    def __init__(self, raw_profile: Dict):
        del raw_profile["name"]
        for key, val in raw_profile.items():
            setattr(self, key, val)


@dataclass
class GroupInfo:
    """
    More info can be found via url:
    https://localapi-doc-en.adspower.com/docs/zSjKAy
    """

    group_id: str
    remark: Optional[str] = ""

    def __init__(self, raw_group: Dict):
        del raw_group["group_name"]
        for key, val in raw_group.items():
            setattr(self, key, val)


@dataclass
class Browser:
    """
    More info can be found via url:
    https://localapi-doc-en.adspower.com/docs/FFMFMf
    """

    cdp_http: str
    cdp_wss: str
    webdriver: str


    @classmethod
    def from_json(cls, json: Dict):
        data = json.get("data")

        ws = data.get("ws")

        cdp_http = ws.get("selenium", "")
        cdp_wss = ws.get("puppeteer", "")
        webdriver = data.get("webdriver", "")

        return Browser(cdp_http, cdp_wss, webdriver)



@dataclass
class ProxyConfig:
    """
    More info can be found via url:
    https://localapi-doc-en.adspower.com/docs/Lb8pOg
    """

    def __init__(
        self,
        soft: str,
        type: Optional[str] = "",
        host: Optional[str] = "",
        port: Optional[str] = "",
        user: Optional[str] = "",
        password: Optional[str] = "",
        url: Optional[str] = "",
    ):
        self.soft = soft
        self.type = type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.url = url

    @classmethod
    def default(cls):
        return ProxyConfig(soft="no_proxy")

    @classmethod
    def from_string(cls, type: str, url: str):
        o = urlparse(url)
        return ProxyConfig(type, o.scheme, o.hostname, o.port, o.username, o.password)

    @classmethod
    def from_json(cls, json: Dict):
        return ProxyConfig(
            json.get("proxy_soft", ""),
            json.get("proxy_type", ""),
            json.get("proxy_host", ""),
            json.get("proxy_port", ""),
            json.get("proxy_user", ""),
            json.get("proxy_password", ""),
            json.get("proxy_url", ""),
        )

    def to_json(self) -> Dict:
        json = {"proxy_soft": self.soft}
        if self.soft == "no_proxy":
            return json

        json["proxy_type"] = self.type
        json["proxy_host"] = self.host
        json["proxy_port"] = self.port
        json["proxy_user"] = self.user
        json["proxy_password"] = self.password
        json["proxy_url"] = self.url

        return json


@dataclass
class FingerprintConfig:
    """
    More info can be found via url:
    https://localapi-doc-en.adspower.com/docs/Awy6Dg
    """

    def __init__(
        self,
        automatic_timezone: Optional[str] = "1",
        timezone: Optional[str] = "",
        webrtc: Optional[str] = "disabled",
        location: Optional[str] = "ask",
        location_switch: Optional[str] = "1",
        longitude: Optional[str] = None,
        latitude: Optional[str] = None,
        accuracy: Optional[str] = "1000",
        language: Optional[List[str]] = ["en-US", "en"],
        language_switch: Optional[str] = "0",
        page_language_switch: Optional[str] = "0",
        page_language: Optional[str] = "en-US",
        ua: Optional[str] = "-",
        screen_resolution: Optional[str] = "none",
        fonts: Optional[List[str]] | str = None,
        canvas: Optional[str] = "1",
        webgl_image: Optional[str] = "1",
        webgl: Optional[str] = "3",
        webgl_config: str = {"unmasked_vendor": "", "unmasked_renderer": ""},
        audio: Optional[str] = "1",
        do_not_track: Optional[str] = "default",
        hardware_concurrency: Optional[str] = "4",
        device_memory: Optional[str] = "8",
        flash: Optional[str] = "block",
        scan_port_type: Optional[str] = "1",
        allow_scan_ports: Optional[str] | str = None,
        media_devices: Optional[str] = "1",
        media_devices_num: Optional[Dict] = {
            "audioinput_num": "1",
            "videoinput_num": "1",
            "audiooutput_num": "1",
        },
        client_rects: Optional[str] = "1",
        device_name_switch: Optional[str] = "1",
        device_name: Optional[str] = None,
        random_ua: Optional[str] = {
            "ua_browser": ["chrome"],
            "ua_version": ["117"],
            "ua_system_version": ["Linux"],
        },
        speech_switch: Optional[str] = "1",
        mac_address_config: Optional[Dict] = {"model": "1", "address": ""},
        browser_kernel_config: Optional[Dict] = {
            "version": "116",
            "type": "chrome",
        },
        gpu: Optional[str] = "0",
    ):
        self.automatic_timezone = automatic_timezone
        self.timezone = timezone
        self.webrtc = webrtc
        self.location = location
        self.location_switch = location_switch
        self.longitude = longitude
        self.latitude = latitude
        self.accuracy = accuracy
        self.language = language
        self.language_switch = language_switch
        self.page_language_switch = page_language_switch
        self.page_language = page_language
        self.ua = ua
        self.screen_resolution = screen_resolution
        self.fonts = fonts
        self.canvas = canvas
        self.webgl_image = webgl_image
        self.webgl = webgl
        self.webgl_config = webgl_config
        self.audio = audio
        self.do_not_track = do_not_track
        self.hardware_concurrency = hardware_concurrency
        self.device_memory = device_memory
        self.flash = flash
        self.scan_port_type = scan_port_type
        self.allow_scan_ports = allow_scan_ports
        self.media_devices = media_devices
        self.media_devices_num = media_devices_num
        self.client_rects = client_rects
        self.device_name_switch = device_name_switch
        self.device_name = device_name
        self.random_ua = random_ua
        self.speech_switch = speech_switch
        self.mac_address_config = mac_address_config
        self.browser_kernel_config = browser_kernel_config
        self.gpu = gpu

    @classmethod
    def default(cls):
        return FingerprintConfig()

    def to_json(self) -> Dict:
        json = self.__dict__
        return {key: value for key, value in json.items() if value is not None}
