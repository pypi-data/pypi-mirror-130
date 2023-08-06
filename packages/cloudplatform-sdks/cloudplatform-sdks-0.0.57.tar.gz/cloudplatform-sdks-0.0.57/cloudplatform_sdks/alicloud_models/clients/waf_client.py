from .client import AliCloudClient
from aliyunsdksemawaf.request.v20200701 import CreateInternetVipRequest, DeleteInternetVipRequest, \
    DescribeInternetVipRequest, CreateWebsiteRequest, DeleteWebsiteRequest, DescribeWebsiteRequest, \
    UploadSSLCertRequest, EditSSLCertRequest, DeleteSSLCertRequest, DescribeSSLCertRequest, EditWebsiteRequest


class WAFClient(AliCloudClient):
    def __init__(self, secret_id, secret_key, region, config):
        super(WAFClient, self).__init__(secret_id, secret_key, region, config, 'semawaf')

    def create_internet_vip(self, query_params=None, body_params=None):
        return self.do_request(CreateInternetVipRequest.CreateInternetVipRequest, query_params, body_params)

    def delete_internet_vip(self, query_params=None, body_params=None):
        return self.do_request(DeleteInternetVipRequest.DeleteInternetVipRequest, query_params, body_params)

    def desc_internet_vip(self, query_params=None, body_params=None):
        return self.do_request(DescribeInternetVipRequest.DescribeInternetVipRequest, query_params, body_params)

    def create_site(self, set_params=None):
        return self.do_request(CreateWebsiteRequest.CreateWebsiteRequest, set_params=set_params)

    def edit_site(self, query_params=None, body_params=None):
        return self.do_request(EditWebsiteRequest.EditWebsiteRequest, query_params, body_params)

    def delete_site(self, set_params):
        return self.do_request(DeleteWebsiteRequest.DeleteWebsiteRequest, set_params=set_params)

    def desc_site(self, query_params=None, body_params=None):
        return self.do_request(DescribeWebsiteRequest.DescribeWebsiteRequest, query_params, body_params)

    def create_ssl_cert(self, query_params=None, body_params=None):
        return self.do_request(UploadSSLCertRequest.UploadSSLCertRequest, query_params, body_params)

    def edit_ssl_cert(self, query_params=None, body_params=None):
        return self.do_request(EditSSLCertRequest.EditSSLCertRequest, query_params, body_params)

    def desc_ssl_cert(self, query_params=None, body_params=None):
        return self.do_request(DescribeSSLCertRequest.DescribeSSLCertRequest, query_params, body_params)

    def delete_ssl_cert(self, set_params):
        return self.do_request(DeleteSSLCertRequest.DeleteSSLCertRequest, set_params=set_params)

