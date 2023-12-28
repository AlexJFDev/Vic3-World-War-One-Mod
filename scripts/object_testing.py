from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot




states = ClausewitzRoot('STATES')

minsk = ClausewitzObject()
create = ClausewitzObject()
create.add_named_value('country', 'c:RUS')
owned = ClausewitzObject()
owned.add_anonymous_values('x0161E0', 'x2B4670', 'xA16195', 'xC9C7AF', 'x51F4A4', 'x26722B', 'x557F9F', 'xC3D50D', 'x21175E', 'x28C9D9', 'x80E061', 'x2EB844', 'xEDA68C', 'x4B3105', 'xC06C1A', 'xA36969', 'x0A89D7', 'x716052', 'xF05D59', 'x16A8B5', 'x80DFDF')
create.add_named_value('owned_provinces', owned)
minsk.add_named_value('create_state', create)
minsk.add_named_value('add_homeland', 'cu:russian')
minsk.add_named_value('add_homeland', 'cu:byelorussian')

states.add_named_value('s:STATE_MINSK', minsk)

print(states.unparse(separator = '    '))
#print(create.unparse())

test = ClausewitzRoot('TEST')
test.add_anonymous_values('x0161E0', 'x2B4670', 'xA16195', 'xC9C7AF', 'x51F4A4', 'x26722B', 'x557F9F', 'xC3D50D', 'x21175E', 'x28C9D9', 'x80E061', 'x2EB844', 'xEDA68C', 'x4B3105', 'xC06C1A', 'xA36969', 'x0A89D7', 'x716052', 'xF05D59', 'x16A8B5', 'x80DFDF')

#print(test.unparse())