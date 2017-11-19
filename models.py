import flask2mongo
from functools import wraps
from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, globals, Response


class BuildStage(flask2mongo.Document):
    stage_order = flask2mongo.IntegerField()

    identifier_key = 'stage_order'

    @staticmethod
    def query_devices(stage_order):
        return {'build_stage': int(stage_order)}

    @staticmethod
    def get_air_conditioners(stage_order, jsoned=False):
        return BuildStage.query(BuildStage.query_devices(stage_order), collection=AirConditioning.__class__.__name__.lower(), jsoned=jsoned)

    @staticmethod
    def get_thermometers(stage_order, jsoned=False):
        return BuildStage.query(BuildStage.query_devices(stage_order), collection=Thermometer.__class__.__name__.lower(), jsoned=jsoned)

    @staticmethod
    def get_bulbs(stage_order, jsoned=False):
        return BuildStage.query(BuildStage.query_devices(stage_order), collection=Bulb.__class__.__name__.lower(), jsoned=jsoned)

    @staticmethod
    def get_electronic_closure(stage_order, jsoned=False):
        return BuildStage.query(BuildStage.query_devices(stage_order), collection=ElectronicClosure.__class__.__name__.lower(), jsoned=jsoned)


class Device(flask2mongo.Document):
    device_id = flask2mongo.ApiKeyField()
    stage_order = flask2mongo.IntegerField()

    identifier_key = 'device_id'
    hybrid = True

    def get_state(self):
        pass

    def set_state(self, value):
        pass

    def save(self, collection=None):
        if not BuildStage.query({'stage_order': self.stage_order.value}):
            raise Exception("This stage doesn't exist")
        super(Device, self).save(collection=collection)


class AirConditioning(Device):
    air_temperature = flask2mongo.IntegerField()

    def get_state(self):
        return self.air_temperature.value

    def set_state(self, value):
        self.air_temperature.value = value


class Thermometer(Device):

    @property
    def temperature(self):
        air_conditioners = BuildStage.get_air_conditioners(self.stage_order.value)
        total_temp = 0.0
        for ac in air_conditioners:
            total_temp += ac.air_temperature
        return total_temp / float(len(air_conditioners))

    def get_state(self):
        return self.temperature

    def set_state(self, value):
        raise Exception('Thermometers cannot be seted')


class Bulb(Device):
    turned_on = flask2mongo.BooleanField()

    def flip(self):
        self.turned_on = not self.turned_on

    def get_state(self):
        return 'On' if self.turned_on else 'Off'

    def set_state(self, value):
        if value:
            self.turned_on = True
        else:
            self.turned_on = False


class ElectronicClosure(Device):
    closed = flask2mongo.BooleanField()

    def invert(self):
        self.closed = not self.closed

    def get_state(self):
        return self.closed

    def set_state(self, value):
        if value:
            self.closed = True
        else:
            self.closed = False


class SDNAdmin(flask2mongo.Document):
    username = flask2mongo.StringField()
    password = flask2mongo.PasswordField(validator='.{8,}')

    identifier_key = 'username'

    @staticmethod
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not globals.session.get('email'):
                return redirect(url_for('viewsbp.login'))
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def check_auth(username, password):
        collection = SDNAdmin.collection
        try:
            sdnadmin_cursor = flask2mongo.MONGO_DB[collection].find({SDNAdmin.username: username})
            sdnadmin = sdnadmin_cursor[0]
            return check_password_hash(sdnadmin.get('password'), password)
        except IndexError:
            return False
