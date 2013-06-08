# Organism - A highly modular and extensible outliner.
# Copyright (C) 2011-2013 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Organism.
#
# Organism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Organism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Organism.  If not, see <http://www.gnu.org/licenses/>.

_RULE_NAME = 'except_once'


def make_rule(start, end, inclusive):
    return {'rule': _RULE_NAME,
            'start': start,
            'end': end,
            'inclusive': inclusive}


def get_occurrences_range(mint, maxt, filename, id_, rule, occs):
    start = rule['start']
    end = rule['end']
    inclusive = rule['inclusive']

    if start <= maxt and end >= mint:
        # The rule is checked in wxscheduler_basicrules.except_once, no need to
        # use occs.except_
        occs.except_safe(filename, id_, start, end, inclusive)


def get_next_item_occurrences(filename, id_, rule, occs):
    start = rule['start']
    end = rule['end']
    inclusive = rule['inclusive']

    limits = occs.get_time_span()
    minstart = limits[0]
    maxend = limits[1]

    if start <= maxend and end >= minstart:
        # The rule is checked in wxscheduler_basicrules.except_once, no need to
        # use occs.except_
        occs.except_safe(filename, id_, start, end, inclusive)
