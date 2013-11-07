##
#     Project: BlueWho
# Description: Information and notification of new discovered bluetooth devices.
#      Author: Fabio Castelli (Muflone) <webreg@vbsimple.net>
#   Copyright: 2009-2013 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import os.path
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from bluewho.constants import *
from bluewho.functions import *

class ModelDevices(object):
  COL_ICON = 0
  COL_CLASS = 1
  COL_TYPE = 2
  COL_TYPE_TRANSLATED = 3
  COL_SUBTYPE = 4
  COL_SUBTYPE_TRANSLATED = 5
  COL_NAME = 6
  COL_ADDRESS = 7
  COL_LASTSEEN = 8
  def __init__(self, model, settings, btsupport):
    self.model = model
    self.settings = settings
    self.btsupport = btsupport

  def clear(self):
    "Clear the model"
    return self.model.clear()

  def add_device(self, address, name, device_class, time, notify):
    "Add a new device to the list and pops notification"
    minor_class, major_class, services_class = self.btsupport.get_classes(device_class)
    device_type = self.btsupport.get_device_type(major_class)
    icon_filename, device_subtype = self.btsupport.get_device_detail(
      major_class, minor_class)
    if device_subtype == 'adapter':
      device_type = 'adapter'
    icon_path = os.path.join(DIR_BT_ICONS, icon_filename)
    if not os.path.isfile(icon_path):
      icon_path = os.path.join(DIR_BT_ICONS, 'unknown.png')

    return self.model.append([
      GdkPixbuf.Pixbuf.new_from_file(icon_path),
      device_class,
      device_type,
      _(device_type),
      device_subtype,
      _(device_subtype),
      name,
      address,
      time
    ])
#  if notify:
#    if settings.get('play sound'):
#      playSound()
#    if settings.get('show notification'):
#      command = settings.get('notify cmd').replace('\\n', '\n') % {
#        'icon': iconPath, 'name': name and name or '', 'address': address }
#      proc = subprocess.Popen(command, shell=True)
#      proc.communicate()

  def path_from_iter(self, treeiter):
    "Get path from iter"
    return type(treeiter) is Gtk.TreeModelRow and treeiter.path or treeiter

  def get_model_data(self, treeiter, column):
    "Get the data from a column of a treeiter"
    return self.model[self.path_from_iter(treeiter)][column]

  def get_name(self, treeiter):
    "Get the device name"
    return self.get_model_data(treeiter, self.__class__.COL_NAME)

  def get_class(self, treeiter):
    "Get the device class"
    return self.get_model_data(treeiter, self.__class__.COL_CLASS)

  def get_type(self, treeiter):
    "Get the device type (untranslated)"
    return self.get_model_data(treeiter, self.__class__.COL_TYPE)

  def get_subtype(self, treeiter):
    "Get the device sub type (untranslated)"
    return self.get_model_data(treeiter, self.__class__.COL_SUBTYPE)

  def get_address(self, treeiter):
    "Get the device address"
    return self.get_model_data(treeiter, self.__class__.COL_ADDRESS)

  def get_last_seen(self, treeiter):
    "Get the device last seen date"
    return self.get_model_data(treeiter, self.__class__.COL_LASTSEEN)

  def __iter__(self):
    "Iter over the whole model rows"
    for each in self.model:
      yield self.model[each.path]

  def __len__(self):
    "Get the devices count"
    return len(self.model)
