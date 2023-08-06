import requests
from authlib.jose import jwt, jwk, util, errors, JsonWebKey, KeySet
import authlib
import logging

logger = logging.getLogger(__name__)

class ValidatorBase:
    def validate_token(self, token, issuer, method=None, 
                        audiences=None, allowed_roles=None):
        raise NotImplementedError


class AsymmetricKeyValidator(ValidatorBase):
    def __init__(self, default_key=None, key_url=None,
                 scope_claim=None, roles_claim=None):
        self.key_url = key_url
        self.roles_claim = roles_claim
        self.scope_claim = scope_claim
        self._keyset = KeySet([])


    def validate_token(self, token, issuer, method=None, audiences=None, allowed_roles=None):
        key = self.get_key(token)
        if not key:
            return (False, None, None, None)

        options = {}

        if audiences:
            if isinstance(audiences, str):
                options["aud"] = {"essential": True, "value": audiences}
            else:
                options["aud"] = {"essential": True, "values": audiences}
        else:
            options["aud"] = {"essential": False, "values": []}
            
        if issuer:
            options["iss"] = {"essential": True, "value": issuer}

        try:
            claims = jwt.decode(token, key, claims_options=options)
            claims.validate()
        except:
            return (False, None, None, None)
        
        payload = dict(claims)
        account_id = payload.get('sub')  # Get account id

        roles = None

        # Check scope is configured and add append it to the roles
        if self.scope_claim and payload.get(self.scope_claim):
            scope = payload.get(self.scope_claim)
            roles = scope.split(" ")

        # If roles claim is defined, gather roles from the token
        if self.roles_claim:
            roles = payload.get(self.roles_claim, []) + (roles or [])

        # Check roles if scope or role claim is set
        if allowed_roles and roles is not None:
            if not any(role in roles for role in allowed_roles):
                return (False, payload, account_id, roles)

        return (True, payload, account_id, roles)

    def get_key(self, token):
        kid = ""
        try:
            header_str = authlib.common.encoding.urlsafe_b64decode(token.split(".")[0].encode()).decode('utf-8')
            header = authlib.common.encoding.json_loads(header_str)
            kid = header["kid"]
            return self._keyset.find_by_kid(kid)
        except Exception as e:
            logger.debug(str(e))
            kid = ""
        try:
            self.fetch_keys()
            return self._keyset.find_by_kid(kid)
        except Exception as e:
            logger.debug(str(e))
            return False

    def fetch_keys(self):
        if not self.key_url:
            return
        response = requests.get(self.key_url)
        if response.ok:
            data = response.json()
            self._keyset = JsonWebKey.import_key_set(data)
