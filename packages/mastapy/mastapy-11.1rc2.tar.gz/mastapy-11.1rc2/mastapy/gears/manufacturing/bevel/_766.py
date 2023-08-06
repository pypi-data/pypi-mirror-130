'''_766.py

Wheel
'''


from mastapy.gears.manufacturing.bevel.cutters import _770
from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _776, _777, _778
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_WHEEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'Wheel')


__docformat__ = 'restructuredtext en'
__all__ = ('Wheel',)


class Wheel(_0.APIBase):
    '''Wheel

    This is a mastapy class.
    '''

    TYPE = _WHEEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Wheel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_finish_cutter(self) -> '_770.WheelFinishCutter':
        '''WheelFinishCutter: 'WheelFinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_770.WheelFinishCutter)(self.wrapped.WheelFinishCutter) if self.wrapped.WheelFinishCutter is not None else None

    @property
    def basic_conical_gear_machine_settings(self) -> '_776.BasicConicalGearMachineSettings':
        '''BasicConicalGearMachineSettings: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _776.BasicConicalGearMachineSettings.TYPE not in self.wrapped.BasicConicalGearMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast basic_conical_gear_machine_settings to BasicConicalGearMachineSettings. Expected: {}.'.format(self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BasicConicalGearMachineSettings.__class__)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings is not None else None

    @property
    def basic_conical_gear_machine_settings_of_type_basic_conical_gear_machine_settings_formate(self) -> '_777.BasicConicalGearMachineSettingsFormate':
        '''BasicConicalGearMachineSettingsFormate: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _777.BasicConicalGearMachineSettingsFormate.TYPE not in self.wrapped.BasicConicalGearMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast basic_conical_gear_machine_settings to BasicConicalGearMachineSettingsFormate. Expected: {}.'.format(self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BasicConicalGearMachineSettings.__class__)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings is not None else None

    @property
    def basic_conical_gear_machine_settings_of_type_basic_conical_gear_machine_settings_generated(self) -> '_778.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'BasicConicalGearMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _778.BasicConicalGearMachineSettingsGenerated.TYPE not in self.wrapped.BasicConicalGearMachineSettings.__class__.__mro__:
            raise CastException('Failed to cast basic_conical_gear_machine_settings to BasicConicalGearMachineSettingsGenerated. Expected: {}.'.format(self.wrapped.BasicConicalGearMachineSettings.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BasicConicalGearMachineSettings.__class__)(self.wrapped.BasicConicalGearMachineSettings) if self.wrapped.BasicConicalGearMachineSettings is not None else None
