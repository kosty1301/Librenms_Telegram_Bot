import requests

from exceptions import LibrenmsApiError
from settings import TRY_RUN_MODULE


def is_ipv4(ip):
    pieces = ip.split('.')
    if len(pieces) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


class LibreNMSAPI:
    def __init__(self, auth_token, request_headers, api_url):
        self.api_url = api_url
        self.headers = request_headers
        self.auth_token = auth_token

    # not used
    def get_alert_rule(self, rule_id):
        req = self.api_url + "rules/" + str(rule_id)
        return requests.get(req, headers=self.headers).json()["rules"][0]

    # not used
    def get_alert(self, alert_id):
        req = self.api_url + "alert/" + str(alert_id)

        return requests.get(req, headers=self.headers).json()

    def list_alerts(self, state="ALL"):
        if state == "ALL":
            req = self.api_url + "alerts"
        else:
            req = self.api_url + "alerts?state=" + state

        return requests.get(req, headers=self.headers).json()

    def get_device(self, device_id):
        req = self.api_url + "devices/" + str(device_id)

        return requests.get(req, headers=self.headers).json()["devices"][0]

    def list_devices(self):
        req = self.api_url + "devices"
        return requests.get(req, headers=self.headers).json()

    def list_services(self):
        req = self.api_url + "services"
        return requests.get(req, headers=self.headers).json()["devices"]

    @staticmethod
    def translate_device_ip_to_sysname(device):
        hostname = device["hostname"]
        if is_ipv4(hostname):
            return device["sysName"]
        return device["hostname"]

    def get_id_and_name_list(self, check_alert=None):
        result = {}
        try:
            devices = self.list_devices()['devices']
        except Exception:
            raise LibrenmsApiError
        for device in devices:
            name = device["sysName"]
            dev_id = device["notes"]
            if name is None or dev_id is None:
                continue
            if not check_alert:
                result.update({dev_id: name})

            if device["status_reason"] == "icmp":
                if device["ignore"] == 0 or device["disabled"] == 0:
                    result.update({dev_id: name})
        return result

    def get_alert_devices(self):
        return self.get_id_and_name_list(check_alert=True)


if __name__ == '__main__':
    print(TRY_RUN_MODULE)
