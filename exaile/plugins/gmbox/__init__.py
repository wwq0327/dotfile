#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gmbox - Google music box
# Copyright (C) 2010 gmbox team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

if __name__ == "gmbox":
    from exaile_panel import ExailePanel
    from xl import event
    
    exaile_panel = None
     
    def enable(exaile):
        if (exaile.loading):
            event.add_callback(_enable, 'exaile_loaded')
        else:
            _enable(None, exaile, None)
     
    def disable(exaile):
        exaile.gui.remove_panel(exaile_panel._child)
     
    def _enable(eventname, exaile, nothing):
        global exaile_panel     
        exaile_panel = ExailePanel(exaile)
        exaile.gui.add_panel(*exaile_panel.get_panel()) 