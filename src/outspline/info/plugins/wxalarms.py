# Outspline - A highly modular and extensible outliner.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Outspline.
#
# Outspline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Outspline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Outspline.  If not, see <http://www.gnu.org/licenses/>.

authors = ("Dario Giovannetti <dev@dariogiovannetti.net>", )
version = "1.4"
description = ("Shows an alarm window whenever an item event/task happens, "
                        "and gives the possibility to snooze or dismiss it.")
website = "https://kynikos.github.io/outspline/"
dependencies = (("core", 4), ("extensions.organism_alarms", 1),
                ("interfaces.wxgui", 3))
optional_dependencies = (("plugins.wxtrayicon", 1), )
