import flask2mongo
from functools import wraps
from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, globals, Response


class Device(flask2mongo.Document):
    device_id = flask2mongo.IntegerField()
    # stage_order = flask2mongo.IntegerField()

    identifier_key = 'device_id'
    hybrid = True

    def get_state(self):
        pass

    def set_state(self, value):
        pass

    # def save(self, collection=None):
    #     if not BuildStage.query({'stage_order': self.stage_order.value}):
    #         raise Exception("This stage doesn't exist")
    #     super(Device, self).save(collection=collection)


class AirConditioning(Device):
    air_temperature = flask2mongo.FloatField()

    def get_state(self):
        return self.air_temperature.value

    def set_state(self, value):
        self.air_temperature.value = value


class Thermometer(Device):
    temperature = flask2mongo.FloatField()

    # @property
    # def temperature(self):
    #     air_conditioners = BuildStage.get_air_conditioners(self.stage_order.value)
    #     total_temp = 0.0
    #     for ac in air_conditioners:
    #         total_temp += ac.air_temperature
    #     return total_temp / float(len(air_conditioners))

    def get_state(self):
        return self.temperature.value

    def set_state(self, value):
        self.temperature.value = float(value)


class Bulb(Device):
    turned_on = flask2mongo.BooleanField()

    def flip(self):
        self.turned_on = not self.turned_on

    def get_state(self):
        return 'Off' if self.turned_on else 'On'

    def set_state(self, value):
        print("AQUI", value)
        if value:
            self.turned_on.value = True
        else:
            self.turned_on.value = False


class ElectronicClosure(Device):
    closed = flask2mongo.BooleanField()

    def invert(self):
        self.closed = not self.closed

    def get_state(self):
        return 'Closed' if self.closed else 'Open'

    def set_state(self, value):
        if value:
            self.closed.value = True
        else:
            self.closed.value = False


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
