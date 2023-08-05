"""HomeKit Button Accessory for Wake On LAN."""
import logging as log
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH
from pywol import wake
from .network import get_ip, ping
from pyhapwol import __version__


class Switch(Accessory):
    """Switch Accessory to send Wake On LAN in HomeKit."""

    category = CATEGORY_SWITCH

    def __init__(self, item, *args, **kwargs):
        """Initialize and bind Switch Accessory to a MAC."""
        super().__init__(*args, **kwargs)
        super().set_info_service(str(__version__), 'RabelCraft',
                                 'PyHAP Switch', 'SW-WoL-01')
        self.__service = self.add_preload_service('Switch')
        self.__on = self.__service.configure_char(
            'On',
            setter_callback=self._set_on)
        self.__fix_ip = 'ip' in item
        self.__ip_address = item['ip'] if 'ip' in item else None
        self.__name = item['name']
        self.__mac = item['mac'].lower()
        self.__port = item['port'] if 'port' in item else 9
        self.__broadcast = item['broadcast']
        self.__interface = item['interface'] if 'interface' in item else None

    def _set_on(self, value):
        if value == 1:
            if not self._get_real_value():
                result = wake(self.__mac, ip_address=self.__broadcast,
                              port=self.__port, return_dest=True)
                log.info('WoL sent to %s.', result)
        else:
            if not self.__fix_ip:
                self.__ip_address = None

    @Accessory.run_at_interval(30)
    def run(self):
        self.__on.set_value(self._get_real_value())

    def _get_real_value(self):
        if self._ensure_ip() is None:
            return False
        return ping(self.__ip_address)

    def _ensure_ip(self):
        if self.__ip_address is None:
            self.__ip_address = get_ip(self.__mac, self.__broadcast,
                                       self.__interface)
            log.info(f'IP Address for {self.__name} [{self.__mac}] '
                     f'is {self.__ip_address}')
        return self.__ip_address
