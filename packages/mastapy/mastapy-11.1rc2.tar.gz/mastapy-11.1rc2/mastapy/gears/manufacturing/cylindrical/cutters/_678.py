'''_678.py

CylindricalFormedWheelGrinderDatabase
'''


from mastapy.gears.manufacturing.cylindrical import _565
from mastapy.gears.manufacturing.cylindrical.cutters import _680
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalFormedWheelGrinderDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalFormedWheelGrinderDatabase',)


class CylindricalFormedWheelGrinderDatabase(_565.CylindricalCutterDatabase['_680.CylindricalGearFormGrindingWheel']):
    '''CylindricalFormedWheelGrinderDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_FORMED_WHEEL_GRINDER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalFormedWheelGrinderDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
