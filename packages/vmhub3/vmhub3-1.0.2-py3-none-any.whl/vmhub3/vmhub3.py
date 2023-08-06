import sys
import requests
import xmltodict
import json
import logging
import argparse
import getpass

logger = logging.getLogger(__name__)


class VMHub3:

    def __init__(self, ip, password):
        self.ip = ip
        self.password = password
        self.cookies = {}

    def __del__(self):
        if "SID" in self.cookies:
            self.disconnect()

    def url(self, action):
        if action == "get":
            return f"http://{self.ip}/xml/getter.xml"
        if action == "set":
            return f"http://{self.ip}/xml/setter.xml"
        if action == "login":
            return f"http://{self.ip}/common_page/login.html"
        raise Exception(f"Unknown action '{action}'")

    def connect(self, timeout=6):
        logger.debug(f"Connecting to {self.ip}")

        # Login
        r = requests.get(
            url=self.url("login"),
            timeout=timeout
        )

        # Token
        cookies = r.cookies.get_dict()
        if "sessionToken" not in cookies:
            sys.exit("Session token not found")
        logger.debug("Session token: {}".format(cookies["sessionToken"]))

        # SID
        r = requests.post(
            url=self.url("set"),
            cookies=cookies,
            data={
                "token": cookies["sessionToken"],
                "fun": "15",  # Authenticate
                "Username": "NULL",
                "Password": self.password,
            }
        )
        self.cookies = r.cookies.get_dict()
        sid = r.content.decode().split("=")[-1]
        if not sid.isnumeric():
            logger.debug(r.content)
            sys.exit("Login failed.")

        logger.debug(f"SID: {sid}")
        self.cookies["SID"] = sid
        logger.debug("Session established")

    def get_config(self, fun, description=""):
        description = description or f"Code {fun}"
        r = requests.post(
            url=self.url("get"),
            cookies=self.cookies,
            data={
                "token": self.cookies["sessionToken"],
                "fun": str(fun)
            }
        )
        self.cookies.clear()
        self.cookies.update(r.cookies.get_dict())
        content = xmltodict.parse(r.content)
        logger.debug("{}:\n{}".format(description, json.dumps(content, indent=4)))
        return content

    def disconnect(self):
        logger.info("Logging out")
        requests.post(
            url=self.url("set"),
            cookies=self.cookies,
            data={
                "token": self.cookies["sessionToken"],
                "fun": "16"
            }
        )
        self.cookies.clear()

    def reboot(self):
        logger.info("Rebooting")
        requests.post(
            url=self.url("set"),
            cookies=self.cookies,
            data={
                "token": self.cookies["sessionToken"],
                "fun": "133"
            }
        )

    def get_global_config(self):
        return self.get_config(1, "Global Config")

    def get_language_config(self):
        return self.get_config(3, "Language Config")

    def get_languages(self):
        return self.get_config(21, "Languages")

    def get_wifi_config(self):
        return self.get_config(315, "Wifi Config")

    def get_status(self):
        return self.get_config(500, "Status")

    def get_wps(self):
        return self.get_config(323, "WPS")

    def get_lan(self):
        return self.get_config(123, "LAN")

    def get_wifi_basic_config(self):
        return self.get_config(311, "Basic Wifi Config")

    def get_wifi_state(self):
        return self.get_config(326, "Wifi State")

    def get_wifi_advanced_config(self):
        return self.get_config(300, "Advanced Wifi Config")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True, help="VMHub3 IP address")
    parser.add_argument("--password", help="Optional, VMHub3 password")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.password is None:
        args.password = getpass.getpass()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.DEBUG,
    )
    try:
        vmhub3 = VMHub3(ip=args.ip, password=args.password)
        vmhub3.connect()
        vmhub3.get_global_config()
        vmhub3.get_language_config()
        vmhub3.get_languages()
        vmhub3.get_wifi_state()
        vmhub3.get_wifi_config()
        vmhub3.get_wifi_basic_config()
        vmhub3.get_wifi_advanced_config()
        vmhub3.get_status()
        vmhub3.get_wps()
        vmhub3.get_lan()
        # vmhub3.reboot()

    except Exception as err:
        logger.error(str(err))


if __name__ == "__main__":
    main()
