import binascii
import os
import re
from jose import jwt
from werkzeug.security import generate_password_hash
from flask2mongo.base import Document
from flask2mongo.exceptions import ValidationException


class Field(object):
    def __init__(self, validator=r'.*', fillable=True):
        self.validator = re.compile(validator)
        self._value = None
        self.fillable = fillable

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, str) or isinstance(value, bytes):
            if not self.validator.match(value):
                raise ValidationException("{} doesn't match with regex {}".format(value, self.validator))
        self._value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __unicode__(self):
        return str(self.value)


class StringField(Field):
    pass


class IntegerField(Field):
    @property
    def value(self):
        return int(self._value)

    @value.setter
    def value(self, value):
        self._value = int(value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.value

    def __unicode__(self):
        return self.value


class FloatField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = float(value)


class PasswordField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = generate_password_hash(value)


class EmailField(Field):
    def __init__(self):
        super().__init__(r'(?i)^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$')


class ApiKeyField(Field):
    def __init__(self):
        super(ApiKeyField, self).__init__(fillable=False)
        print(str(binascii.hexlify(os.urandom(24)).decode('utf8')))
        self.value = str(binascii.hexlify(os.urandom(24)).decode('utf8'))


class ApiSecretField(Field):

    secret = 'T\x94 \x03\xd9\x896fF\xcc(\\b4B\x1b\xa2\x92g\xd8\x06\xdc\x1d$'

    def __init__(self, api_key_field: Field):
        api_key = api_key_field.value
        super(ApiSecretField, self).__init__(fillable=False)
        self.value = str(jwt.encode({'key': api_key}, self.secret, algorithm='HS256'))

    @staticmethod
    def check_secret(api_key, api_secret):
        decoded = jwt.decode(api_secret, ApiSecretField.secret, algorithms=['HS256'])
        return decoded.get('key') == api_key


class BooleanField(Field):
    setted_count = 0

    def __bool__(self):
        if self.setted_count == 0: return False
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.setted_count += 1
        self._value = bool(value)
