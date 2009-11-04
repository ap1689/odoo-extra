# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import wizard
import time
import datetime
import pooler

from tools.misc import UpdateableDict

#Fields = UpdateableDict()

Form = """<?xml version="1.0"?>
<form string="Statistic Reports">
   <field name="start_date"/>
   <field name="end_date"/>
   <field name="level"/>
   <field name="result"/>
   <field name="origin_partner"/>
   <group colspan="4"  attrs="{'invisible':[('level','=','offer')]}">
        <field name="campaign_id" attrs="{'required':[('level','=','campaign')]}" />
   </group>
   <group colspan="4"  attrs="{'invisible':[('level','!=','offer')]}">
        <field name="offer_id" attrs="{'required':[('level','=','offer')]}" />
   </group>
   <!--group colspan="4"  attrs="{'invisible':[('level','!=','segment')]}">
        <field name="segment_id" attrs="{'required':[('level','=','segment')]}" />
   </group-->
</form>"""

error_form = """<?xml version="1.0"?>
<form string="Statistic Reports - Date error">
   <label string="End date can not be less than start date"/>
</form>"""

_level_selection = [
        ('campaign','Campaign'),
        ('offer','Commercial Offer'),
        ('segment','Segment')
        ]

_result_selection = [
        ('qty','Quantity'),
        ('amt','Amount'),
        ]

#_level2_selection = [
#        ('step','Offer Step'),
#        ('segment','Segment'),
#        ]

Fields = {
    'start_date' : {'string':'Start Date','type':'date', 'required' : True },
    'end_date' : {'string':'End Date','type':'date', 'required' : True },
    'origin_partner':{'string':'Sort by origin partner' , 'type':'boolean'},
    'level' : {'string': 'Level', 'type': 'selection', 'selection':_level_selection, 'default': lambda *a:"campaign", },
    'result' : {'string': 'Result', 'type': 'selection', 'selection':_result_selection, 'default': lambda *a:"qty"},    
#    'level2' : {'string': 'Level', 'type': 'selection', 'selection':_level2_selection, 'default': lambda *a:"step", },
    'campaign_id' : {'string': 'Campaign', 'type': 'many2one', 'relation': 'dm.campaign',}, 
    'offer_id' : {'string': 'Offer', 'type': 'many2one', 'relation': 'dm.offer', },
#    'segment_id' : {'string': 'Offer', 'type': 'many2one', 'relation': 'dm.campaign.proposition.segment',},
}
    
def _check_date(self, cr, uid, data, context) :
    if data['form']['start_date'] > data['form']['end_date'] :
        return 'error'
    return 'print'

class wizard_statistics_so_all(wizard.interface):
    states = {
        'init': {
            'actions': [],
            'result': {'type':'form', 'arch':Form, 'fields':Fields, 'state':[('end','Cancel'),('check_date','Print Report')]},
        },
        'check_date' :{
            'actions' : [],
            'result' : {'type' : 'choice' , 'next_state': _check_date}
        },
        'error': {
            'actions': [],
            'result': {'type':'form', 'arch':error_form, 'fields':{}, 'state':[('end','Cancel'),('init','Reset Value')]},
        },
        'print': {
            'actions': [],
            'result': {'type':'print', 'report':'dm.statistics.so.all', 'state':'end'},
        },
    }
wizard_statistics_so_all('dm.statistics.so.all')



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
