'''_544.py

CylindricalGearAGMAMaterialDatabase
'''


from mastapy.gears.materials import _547, _538
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'CylindricalGearAGMAMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearAGMAMaterialDatabase',)


class CylindricalGearAGMAMaterialDatabase(_547.CylindricalGearMaterialDatabase['_538.AGMACylindricalGearMaterial']):
    '''CylindricalGearAGMAMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearAGMAMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
