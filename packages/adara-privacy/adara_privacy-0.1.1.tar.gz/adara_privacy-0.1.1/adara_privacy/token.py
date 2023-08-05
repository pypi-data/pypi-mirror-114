import hashlib

from adara_privacy.utils import (
    sdk_config,
)

import adara_privacy

KEY_TOKEN_TYPE = 'type'
KEY_TOKEN_COMMON = 'common'
KEY_TOKEN_PRIVATE = 'private'


def _tokenize(value: str, salt: str) -> str:
    return hashlib.sha256(str(salt + hashlib.sha256(value.encode()).hexdigest()).encode()).hexdigest()


class Token():
    def __init__(self, *args, identifier=None, token_dict: dict = None):
        super().__init__()
        self._identifier = None
        self._common_tokens = None
        self._private = None

        if len(args) == 1:
            if identifier or token_dict:
                raise ValueError("Token constructor accepts a single input and multiple were given.")
            if isinstance(args[0], adara_privacy.Identifier):
                identifier = args[0]
            elif isinstance(args[0], dict):
                token_dict = args[0]
            else:
                raise TypeError("Token constructor only accepts either an Identifier instance or dict.")
        elif len(args) > 1:
            raise ValueError("Token constructor accepts a single input and multiple were given.")

        if identifier and token_dict:
            raise ValueError("Token constructor accepts a single input and multiple were given.")
        elif not (identifier or token_dict):
            raise ValueError("Token constructor requires a single input but none was given.")

        if isinstance(identifier, adara_privacy.Identifier):
            self._identifier = identifier
        elif isinstance(token_dict, dict):
            self._common_tokens = dict()
            # try:
            #     self._common = token_dict[KEY_TOKEN_COMMON]
            # except KeyError:
            #     raise ValueError('Argument "token_dict" was passed an invalid token definition: key "common" is required.')
            try:
                self._identifier_type = token_dict[KEY_TOKEN_TYPE]
            except KeyError:
                self._identifier_type = adara_privacy.Identifier.KEY_GENERIC_IDENTIFIER
            # try:
            #     assert self.private == token_dict[KEY_TOKEN_PRIVATE]
            # except KeyError:
            #     pass
            # except AssertionError:
            #     raise ValueError('Value for key "private" does not match expected salted token for "common" value.')
        else:
            raise Exception('Token() was not passed arguments required for instantiation.')

    @property
    def identifier_type(self):
        return self._identifier.identifier_type if self._identifier else self._identifier_type

    @property
    def common(self):
        if self._common_tokens is None:
            self._common_tokens = {k: _tokenize(self._identifier.tokenization_value, sdk_config.privacy.common_salts[k]) for k in sdk_config.privacy.common_salts}
        return self._common_tokens

    @property
    def private(self):
        if not self._private:
            self._private = _tokenize(self._identifier.tokenization_value, sdk_config.privacy.private_salt)
        return self._private

    def to_dict(self):
        tokens = {KEY_TOKEN_PRIVATE: self.private, **self.common}
        if self._identifier.common_tokens:
            tokens = {k: tokens[k] for k in tokens if k in set(self._identifier.common_tokens)}

        metadata = {KEY_TOKEN_TYPE: self.identifier_type}
        if self._identifier.label:
            metadata['label'] = self._identifier.label

        return {**tokens, **metadata}
