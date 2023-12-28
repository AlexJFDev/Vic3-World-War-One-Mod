from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

root = ClausewitzRoot('', name_values={
    'STATES': [ClausewitzObject(name_values={
        's:STATE_MINSK': [ClausewitzObject(name_values={
            'create_state': [ClausewitzObject(name_values={
                'owned_provinces': [ClausewitzObject(
                    anonymous_values=['x0161E0', 'x2B4670', 'xA16195', 'xC9C7AF', 'x51F4A4', 'x26722B', 'x557F9F', 'xC3D50D', 'x21175E', 'x28C9D9', 'x80E061', 'x2EB844', 'xEDA68C', 'x4B3105', 'xC06C1A', 'xA36969', 'x0A89D7', 'x716052', 'xF05D59', 'x16A8B5', 'x80DFDF']
                )],
                'country': ['c:RUS']
            })],
            'add_homeland': ['cu:russian', 'cu:byelorussian']
        })],
        's:STATE_LOUISIANA':[ClausewitzObject(name_values={
            'create_state': [ClausewitzObject(name_values={
                'owned_provinces': [ClausewitzObject(
                    anonymous_values=['x39D7A2', 'xC51912', 'x9A7554', 'x13B0C7', 'x4FA3C4', 'x86BC13', 'xC1273E', 'x371B1B', 'xC0F080', 'x0CF7A4', 'x68C793', 'x216122', 'x1BF244', 'x9E96B6', 'xC62139', 'xBF79F5', 'xAC4818', 'x18D465', 'xC07080', 'x131940', 'x71BEC1', 'xEE0FAA', 'x7EF4B8', 'x403095', 'xEFB99C', 'x2BEBAE', 'xD658E7', 'xA4EE3C']
                )],
                'country': ['c:USA']
            })],
            'add_homeland': ['cu:dixie', 'cu:afro_american', 'cu:cajun', 'cu:afro_antillean']
        })]
    })],
})

print(root.unparse(separator = '    '))
