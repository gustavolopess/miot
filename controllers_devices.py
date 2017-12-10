from flask import Blueprint, request, abort, jsonify, session, redirect, url_for, escape, render_template, flash, Response
import models
import traceback
import flask2mongo
import zmq

# Socket to send messages to w_pub
context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5555")

blue_print = Blueprint('controllers_devices', __name__, template_folder='templates')
devices = {
    'air': models.AirConditioning,
    'thermometer': models.Thermometer,
    'closure': models.ElectronicClosure,
    'bulb': models.Bulb
}


value_parser = {
    'air': 'air_temperature',
    'thermometer': 'temperature',
    'closure': 'closed',
    'bulb': 'turned_on'
}


@blue_print.route('/api/device/register/<device>/', methods=['POST'])
def register_device(device):
    try:
        if not request.json:
            abort(400)
        device_id = request.json.get('device_id')
        device_cls = devices[device]
        existent = device_cls.query({'device_id': int(device_id)})
        value = request.json.get('value')
        if device in ['closure', 'bulb']:
            if value == 0:
                value = False
            else:
                value = True
        if len(existent) > 0:
            device_obj = existent[0]
            value = request.json.get('value')
            device_obj.set_state(value)
            device_cls.update(device_obj.jsonify(), {'device_id': device_obj.device_id.value})
            return Response('Device updated')
        creation_dict = dict(request.json).copy()
        creation_dict[value_parser[device]] = value
        del creation_dict['value']
        new_device = devices[device](creation_dict)
        new_device.save()
        return jsonify(new_device.jsonify())
    except Exception as e:
        return Response(str(e) + str(traceback.format_exc()))


@blue_print.route('/api/device/state/<device>/<device_id>/', methods=['GET', 'POST'])
def device_state(device, device_id):
    try:
        dvc_cls = devices.get(device)
        dvc_obj = dvc_cls.query({'device_id': int(device_id)})[0]
        if request.method == 'POST':
            value = request.json.get('value')
            if value == True: value = 1
            elif value == False: value = 0
            msg = str(device+"/"+device_id+"/"+str(value))
            sender.send_string(msg)
            return Response("Enviado. O estado do {} {} é {}".format(dvc_cls.__name__, device_id, value))
        else:
            return jsonify({'state': dvc_obj.get_state()})
    except Exception as e:
        return Response(str(e) + str(traceback.format_exc()))
