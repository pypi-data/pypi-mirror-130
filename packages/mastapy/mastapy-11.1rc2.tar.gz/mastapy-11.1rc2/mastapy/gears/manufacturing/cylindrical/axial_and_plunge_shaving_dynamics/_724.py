'''_724.py

ShavingDynamicsConfiguration
'''


from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _721, _706, _707, _708,
    _713, _714, _710
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_CONFIGURATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsConfiguration',)


class ShavingDynamicsConfiguration(_0.APIBase):
    '''ShavingDynamicsConfiguration

    This is a mastapy class.
    '''

    TYPE = _SHAVING_DYNAMICS_CONFIGURATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conventional_shaving_dynamics(self) -> '_721.ShavingDynamicsCalculation[_706.ConventionalShavingDynamics]':
        '''ShavingDynamicsCalculation[ConventionalShavingDynamics]: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _721.ShavingDynamicsCalculation[_706.ConventionalShavingDynamics].TYPE not in self.wrapped.ConventionalShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ShavingDynamicsCalculation[ConventionalShavingDynamics]. Expected: {}.'.format(self.wrapped.ConventionalShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConventionalShavingDynamics.__class__)(self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics is not None else None

    @property
    def conventional_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_707.ConventionalShavingDynamicsCalculationForDesignedGears':
        '''ConventionalShavingDynamicsCalculationForDesignedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.ConventionalShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.ConventionalShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConventionalShavingDynamics.__class__)(self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics is not None else None

    @property
    def conventional_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_708.ConventionalShavingDynamicsCalculationForHobbedGears':
        '''ConventionalShavingDynamicsCalculationForHobbedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _708.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.ConventionalShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.ConventionalShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConventionalShavingDynamics.__class__)(self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics is not None else None

    @property
    def conventional_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_713.PlungeShavingDynamicsCalculationForDesignedGears':
        '''PlungeShavingDynamicsCalculationForDesignedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _713.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.ConventionalShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.ConventionalShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConventionalShavingDynamics.__class__)(self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics is not None else None

    @property
    def conventional_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_714.PlungeShavingDynamicsCalculationForHobbedGears':
        '''PlungeShavingDynamicsCalculationForHobbedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _714.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.ConventionalShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.ConventionalShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConventionalShavingDynamics.__class__)(self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics is not None else None

    @property
    def plunge_shaving_dynamics(self) -> '_721.ShavingDynamicsCalculation[_710.PlungeShaverDynamics]':
        '''ShavingDynamicsCalculation[PlungeShaverDynamics]: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _721.ShavingDynamicsCalculation[_710.PlungeShaverDynamics].TYPE not in self.wrapped.PlungeShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ShavingDynamicsCalculation[PlungeShaverDynamics]. Expected: {}.'.format(self.wrapped.PlungeShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlungeShavingDynamics.__class__)(self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics is not None else None

    @property
    def plunge_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_707.ConventionalShavingDynamicsCalculationForDesignedGears':
        '''ConventionalShavingDynamicsCalculationForDesignedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.PlungeShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.PlungeShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlungeShavingDynamics.__class__)(self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics is not None else None

    @property
    def plunge_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_708.ConventionalShavingDynamicsCalculationForHobbedGears':
        '''ConventionalShavingDynamicsCalculationForHobbedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _708.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.PlungeShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.PlungeShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlungeShavingDynamics.__class__)(self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics is not None else None

    @property
    def plunge_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_713.PlungeShavingDynamicsCalculationForDesignedGears':
        '''PlungeShavingDynamicsCalculationForDesignedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _713.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in self.wrapped.PlungeShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(self.wrapped.PlungeShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlungeShavingDynamics.__class__)(self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics is not None else None

    @property
    def plunge_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_714.PlungeShavingDynamicsCalculationForHobbedGears':
        '''PlungeShavingDynamicsCalculationForHobbedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _714.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in self.wrapped.PlungeShavingDynamics.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(self.wrapped.PlungeShavingDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlungeShavingDynamics.__class__)(self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics is not None else None
