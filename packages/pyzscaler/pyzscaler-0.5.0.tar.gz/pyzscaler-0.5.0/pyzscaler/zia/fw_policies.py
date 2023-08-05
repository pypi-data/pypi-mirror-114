from restfly.endpoint import APIEndpoint
from box import Box, BoxList


class FirewallPolicyAPI(APIEndpoint):

    def list_dns(self):
        return self._get('firewallDnsRules', box=BoxList)

    def add_dns(self):
        return self._post('firewallDnsRules')

    def detail_dns(self, id: str):
        return self._get(f'firewallDnsRules/{id}')

    def update_dns(self, id: str):
        return self._put(f'firewallDnsRules/{id}')

    def delete_dns(self, id: str):
        return self._delete(f'firewallDnsRules/{id}')

    # Filter rule methods

    def list_filter(self):
        return self._get('firewallFilteringRules', box=BoxList)

    def add_filter(self):
        return self._post('firewallFilteringRules')

    def detail_filter(self, id: str):
        return self._get(f'firewallFilteringRules/{id}')

    def update_filter(self, id: str):
        return self._put(f'firewallFilteringRules/{id}')

    def delete_filter(self, id: str):

        return self._delete(f'firewallFilteringRules/{id}')




