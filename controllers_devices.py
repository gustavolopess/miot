from flask import Blueprint, request, abort, jsonify, session, redirect, url_for, escape, render_template, flash, Response
import models
import traceback

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
        dvc_obj = dvc_cls.query({'device_id': device_id})[0]
        if request.method == 'POST':
            dvc_obj.set_state(request.json.get('value'))
        else:
            return Response(dvc_obj.get_state())
    except Exception as e:
        return Response(str(e))

