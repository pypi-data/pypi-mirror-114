from adara_privacy.identifier import Identifier
from adara_privacy.streamers.streamer import Streamer
from adara_privacy.token import _tokenize
from adara_privacy.utils import sdk_config


class Identity():
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._identifiers = []

        if args and all(isinstance(arg, Identifier) for arg in args):
            for arg in args:
                if not arg.is_empty:
                    self._identifiers.append(arg)
        elif len(args) == 1 and isinstance(args[0], list) and all(isinstance(item, dict) for item in args[0]):
            self._identifiers.extend(Identifier(item) for item in args[0])
        elif len(args) > 0:
            raise TypeError('Arguments passed to constructor must be all of type Identifier, or a single argument as a list of deserializable token dicts.')

        if kwargs and all(isinstance(kwargs[k], (str, int, float)) for k in kwargs):
            self._identifiers.extend([Identifier(kwargs[k], identifier_type=k)] for k in kwargs)

    def add_identifier(self, identifier):
        if isinstance(identifier, Identifier):
            if not identifier.is_empty:
                self._identifiers.append(identifier)
        else:
            raise TypeError('Argument "identifier" must be an instance of type Identifier.')

    @property
    def identifiers(self):
        return list(self._identifiers)

    @property
    def tokens(self):
        return [
            identifier.token for identifier in self._identifiers
        ]

    @property
    def package_token(self):
        return _tokenize(':'.join(sorted({t.private + t.identifier_type for t in self.tokens})), sdk_config.privacy.private_salt)

    def save(self, streamer):
        if not isinstance(streamer, Streamer):
            raise TypeError('Argument "streamer" must be an instance of type "Streamer".')
        streamer.save(self)

    def to_dict(self, format: str = 'identity'):
        if format == 'identity':
            return {
                'package_token': self.package_token,
                'identities': [i.to_dict() for i in self._identifiers]
            }
        elif format == 'token':
            return self.to_tokens()
        else:
            raise ValueError('Argument "format" must be either "identity" (default) or "token".')

    def to_tokens(self):
        return {
            'package_token': self.package_token,
            'tokens': [i.token.to_dict() for i in self._identifiers]
        }

    def __eq__(self, other):
        return True
