from social_core.backends.open_id_connect import OpenIdConnectAuth

class ProloginOpenIdConnect(OpenIdConnectAuth):
    name = "prologin"
    OIDC_ENDPOINT = "https://prologin.org/openid"
