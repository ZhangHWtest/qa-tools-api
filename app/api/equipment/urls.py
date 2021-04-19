# -*- coding: utf-8 -*-

from .views import *
from .views import equipment

equipment.add_url_rule('/manufacturer/list', view_func=ManufacturerList.as_view('manufacturer_list'))
equipment.add_url_rule('/manufacturer/add', view_func=AddManufacturer.as_view('add_manufacturer'))
equipment.add_url_rule('/manufacturer/del', view_func=DelManufacturer.as_view('del_manufacturer'))
equipment.add_url_rule('/equipment/list', view_func=EquipmentList.as_view('equipment_list'))
equipment.add_url_rule('/equipment/info', view_func=EquipmentInfo.as_view('equipment_info'))
equipment.add_url_rule('/equipment/add', view_func=AddEquipment.as_view('add_equipment'))
equipment.add_url_rule('/equipment/edit', view_func=EditEquipment.as_view('edit_equipment'))
equipment.add_url_rule('/equipment/switch', view_func=SwitchEquipment.as_view('switch_equipment'))
equipment.add_url_rule('/equipment/del', view_func=DelEquipment.as_view('del_equipment'))
equipment.add_url_rule('/equipment/log', view_func=EquipmentLogList.as_view('equipment_log_list'))
