from flask import Blueprint, request, abort, jsonify, session, redirect, url_for, escape, render_template, flash, Response
import models
import traceback
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


@blue_print.route('/api/device/register/<device>/', methods=['POST'])
def register_device(device):
    try:
        if not request.json:
            abort(400)
        new_device = devices[device](request.json)
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
            msg = str(device+"/"+device_id+"/"+str(value))
            sender.send_string(msg)
            return Response("Enviado. O estado do {} {} é {}".format(dvc_cls.__name__, device_id, value))
        else:
            return jsonify({'state': dvc_obj.get_state()})
    except Exception as e:
        return Response(str(e) + str(traceback.format_exc()))


@blue_print.route('/api/device/change/state/<device>/<device_id>/', methods=['POST'])
def change_device_state(device, device_id):
    try:
        dvc_cls = devices.get(device)
        dvc_obj = dvc_cls.query({'device_id': int(device_id)})[0]
        value = request.json.get('value')
        dvc_obj.set_state(value)
        dvc_cls.update(dvc_obj.jsonify(), {'device_id': dvc_obj.device_id.value})
        return Response("Enviado. O estado do {} {} é {}".format(dvc_cls.__name__, device_id, value))
    except Exception as e:
        return Response(str(e) + str(traceback.format_exc()))


@blue_print.route('/api/devices/<stage>/', methods=['GET'])
def get_stage_devices(stage):
    resp = {
        'air': models.BuildStage.get_air_conditioners(stage, jsoned=True),
        'thermometer': models.BuildStage.get_thermometers(stage, jsoned=True),
        'closure': models.BuildStage.get_electronic_closure(stage, jsoned=True),
        'bulb': models.BuildStage.get_bulbs(stage, jsoned=True)
    }
    return jsonify(resp)


@blue_print.route('/api/stage/register/<stage>/', methods=['POST'])
def register_stage(stage):
    if int(stage) != 1 and not models.BuildStage.query({'stage_order': int(stage)-1}):
        return Response("The previous stage ({}) doesn't exist. A stage can't be built above nothing.".format(
            int(stage)-1)
        )
    new_stage = models.BuildStage(stage_order=stage)
    new_stage.save()
    return jsonify(new_stage.jsonify())
