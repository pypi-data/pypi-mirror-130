'''_655.py

WormGrindingProcessSimulationNew
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _648, _653, _650, _651,
    _647, _657, _652, _641,
    _654
)
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_WORM_GRINDING_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'WormGrindingProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrindingProcessSimulationNew',)


class WormGrindingProcessSimulationNew(_641.ProcessSimulationNew['_654.WormGrindingProcessSimulationInput']):
    '''WormGrindingProcessSimulationNew

    This is a mastapy class.
    '''

    TYPE = _WORM_GRINDING_PROCESS_SIMULATION_NEW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGrindingProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_grinding_process_lead_calculation(self) -> '_648.WormGrindingLeadCalculation':
        '''WormGrindingLeadCalculation: 'WormGrindingProcessLeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_648.WormGrindingLeadCalculation)(self.wrapped.WormGrindingProcessLeadCalculation) if self.wrapped.WormGrindingProcessLeadCalculation is not None else None

    @property
    def worm_grinding_process_profile_calculation(self) -> '_653.WormGrindingProcessProfileCalculation':
        '''WormGrindingProcessProfileCalculation: 'WormGrindingProcessProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_653.WormGrindingProcessProfileCalculation)(self.wrapped.WormGrindingProcessProfileCalculation) if self.wrapped.WormGrindingProcessProfileCalculation is not None else None

    @property
    def worm_grinding_process_gear_shape_calculation(self) -> '_650.WormGrindingProcessGearShape':
        '''WormGrindingProcessGearShape: 'WormGrindingProcessGearShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_650.WormGrindingProcessGearShape)(self.wrapped.WormGrindingProcessGearShapeCalculation) if self.wrapped.WormGrindingProcessGearShapeCalculation is not None else None

    @property
    def worm_grinding_process_mark_on_shaft_calculation(self) -> '_651.WormGrindingProcessMarkOnShaft':
        '''WormGrindingProcessMarkOnShaft: 'WormGrindingProcessMarkOnShaftCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_651.WormGrindingProcessMarkOnShaft)(self.wrapped.WormGrindingProcessMarkOnShaftCalculation) if self.wrapped.WormGrindingProcessMarkOnShaftCalculation is not None else None

    @property
    def worm_grinding_cutter_calculation(self) -> '_647.WormGrindingCutterCalculation':
        '''WormGrindingCutterCalculation: 'WormGrindingCutterCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_647.WormGrindingCutterCalculation)(self.wrapped.WormGrindingCutterCalculation) if self.wrapped.WormGrindingCutterCalculation is not None else None

    @property
    def worm_grinding_process_total_modification_calculation(self) -> '_657.WormGrindingProcessTotalModificationCalculation':
        '''WormGrindingProcessTotalModificationCalculation: 'WormGrindingProcessTotalModificationCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_657.WormGrindingProcessTotalModificationCalculation)(self.wrapped.WormGrindingProcessTotalModificationCalculation) if self.wrapped.WormGrindingProcessTotalModificationCalculation is not None else None

    @property
    def worm_grinding_process_pitch_calculation(self) -> '_652.WormGrindingProcessPitchCalculation':
        '''WormGrindingProcessPitchCalculation: 'WormGrindingProcessPitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_652.WormGrindingProcessPitchCalculation)(self.wrapped.WormGrindingProcessPitchCalculation) if self.wrapped.WormGrindingProcessPitchCalculation is not None else None
