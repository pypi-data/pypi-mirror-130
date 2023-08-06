from .clients import waf_client


class AliWAF:
    def __init__(self, obj):
        self.obj = obj

    @classmethod
    def get(cls, vip_id):
        vips = waf_client.desc_internet_vip().get('Result', []) or []
        for vip in vips:
            if vip.get('ip') == vip_id:
                return cls(vip)
        return None

    @classmethod
    def list(cls, params=None):
        result = waf_client.desc_internet_vip(params)
        vips = result.get('Result', []) or []
        return [cls(vip) for vip in vips]

    @classmethod
    def create(cls, params):
        return waf_client.create_internet_vip(params)

    def delete(self):
        return waf_client.delete_internet_vip({'Vip': self.external_id})

    @property
    def external_id(self):
        return self.obj.get('ip')

    @property
    def external_name(self):
        return self.obj.get('ip')

    @property
    def ip_type(self):
        return self.obj.get('type')

    @property
    def is_delete(self):
        return self.obj.get('delete')


class AliSSLCert:
    def __init__(self, obj):
        self.obj = obj

    @classmethod
    def get(cls, cert_id):
        cert = waf_client.desc_ssl_cert({'Id': cert_id}).get('Result', {}).get('items')
        if cert:
            return cls(cert[0])
        return None

    @classmethod
    def list(cls, param=None):
        params = {'PageSize': 100}
        if param:
            params.update(param)
        result = waf_client.desc_ssl_cert(params)
        ssl_certs = result.get('Result', {}).get('items', []) or []
        return [cls(cert) for cert in ssl_certs]

    @classmethod
    def create(cls, params):
        return waf_client.create_ssl_cert(params).get('Result', {}).get('id')

    @classmethod
    def edit(cls, params):
        return waf_client.edit_ssl_cert(params).get('Result')

    def delete(self):
        return waf_client.delete_ssl_cert({'IdLists': [self.external_id]})

    @property
    def external_id(self):
        return self.obj.get('id')

    @property
    def external_name(self):
        return self.obj.get('name')

    @property
    def signature(self):
        return self.obj.get('signature')

    @property
    def info(self):
        return self.obj.get('info')

    @property
    def domains(self):
        return self.obj.get('domains')


class AliWebSite:
    def __init__(self, obj):
        self.obj = obj

    @classmethod
    def get(cls, site_id):
        site = waf_client.desc_site({'Id': site_id}).get('Result', {}).get('items')
        if site:
            return cls(site[0])
        return None

    @classmethod
    def list(cls, params=None):
        result = waf_client.desc_site(params)
        vips = result.get('Result', {}).get('items', [])
        return [cls(vip) for vip in vips]

    @classmethod
    def create(cls, set_params):
        return waf_client.create_site(set_params)

    @classmethod
    def edit(cls, params):
        return waf_client.edit_site(params)

    def delete(self):
        return waf_client.delete_site({'IdLists': [self.external_id]})

    @property
    def external_id(self):
        return self.obj.get('id')

    @property
    def external_name(self):
        return self.obj.get('name')

    @property
    def ip(self):
        ip = self.obj.get('ip')
        return ','.join(ip) if ip else ''

    @property
    def tenant_id(self):
        return self.obj.get('tenant_id')

    @property
    def remark(self):
        return self.obj.get('remark')

    @property
    def ports(self):
        ports = self.obj.get('ports') if self.obj.get('ports') else []
        port_list = []
        for port in ports:
            port_list.append(str(port.get('port')))
        return ','.join(port_list) if port_list else ''

    @property
    def policy_rules(self):
        return self.obj.get('policy_rules')

    @property
    def health_check_status(self):
        return self.obj.get('health_check_status')

    @property
    def health_check_config(self):
        return self.obj.get('health_check_config')

    @property
    def vpc(self):
        return self.obj.get('vpc')

    @property
    def vip(self):
        vip = self.obj.get('vip')
        return ','.join(vip) if vip else ''

    @property
    def server_name(self):
        return self.obj.get('server_names')

    @property
    def policy_group(self):
        return self.obj.get('policy_group')

    @property
    def operation_mode(self):
        return self.obj.get('operation_mode')

    @property
    def server_names(self):
        server_names = self.obj.get('server_names')
        return ','.join(server_names) if server_names else ''

    @property
    def x_forwarded_for_action(self):
        return self.obj.get('backend_config', {}).get('x_forwarded_for_action')

    @property
    def load_balance_policy(self):
        return self.obj.get('backend_config', {}).get('load_balance_policy')

    @property
    def servers(self):
        servers = self.obj.get('backend_config', {}).get('servers', [])
        return servers
