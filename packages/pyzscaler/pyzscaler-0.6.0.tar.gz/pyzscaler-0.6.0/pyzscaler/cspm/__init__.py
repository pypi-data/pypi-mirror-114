import os

from restfly.session import APISession

from pyzscaler.utils import obfuscate_api_key
from pyzscaler.version import version


class CSPM(APISession):
    _vendor = 'Zscaler'
    _product = 'Cloud Security Posture Management'
    _build = version
    _box = True
    _box_attrs = {
        'camel_killer_box': True
    }
    _env_base = 'CSPM'
    _url = 'https://trialapi.cloudneeti.com'

    def __init__(self, **kw):
        self._api_key = kw.get('api_key',
                               os.getenv(f'{self._env_base}_API_KEY'))
        self._api_secret = kw.get('api_secret',
                                  os.getenv(f'{self._env_base}'))
        self._app_id = kw.get('app_id',
                                os.getenv(f'{self._env_base}_APP_ID'))
        self._license_id = kw.get('license_id',
                                os.getenv(f'{self._env_base}_LICENSE_ID'))
        super(CSPM, self).__init__(**kw)

    def _build_session(self, **kwargs) -> None:
        super(CSPM, self)._build_session(**kwargs)
        api_obf = obfuscate_api_key(self._api_key)

        payload = {
            'APIApplicationId': self._app_id,

        }
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self._api_key
        }
        self.post(f'authorize/license/{self._license_id}/token', headers=headers, json=payload)


