'''_1991.py

Databases
'''


from mastapy.bearings import _1635
from mastapy._internal import constructor
from mastapy.bolts import _1262, _1264, _1269
from mastapy.gears.gear_set_pareto_optimiser import (
    _875, _876, _879, _880,
    _885, _886, _888, _889,
    _890, _891
)
from mastapy.gears.manufacturing.bevel import _755
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _678, _684, _689, _690
)
from mastapy.gears.manufacturing.cylindrical import _570, _581
from mastapy.gears.materials import (
    _541, _543, _544, _545,
    _548, _555, _562
)
from mastapy.system_model.optimization import _1958, _1967
from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2289
from mastapy.materials import _218, _219, _238
from mastapy.shafts import _25
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DATABASES = python_net_import('SMT.MastaAPI.SystemModel.DatabaseAccess', 'Databases')


__docformat__ = 'restructuredtext en'
__all__ = ('Databases',)


class Databases(_0.APIBase):
    '''Databases

    This is a mastapy class.
    '''

    TYPE = _DATABASES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Databases.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rolling_bearing_database(self) -> '_1635.RollingBearingDatabase':
        '''RollingBearingDatabase: 'RollingBearingDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1635.RollingBearingDatabase)(self.wrapped.RollingBearingDatabase) if self.wrapped.RollingBearingDatabase is not None else None

    @property
    def bolt_geometry_database(self) -> '_1262.BoltGeometryDatabase':
        '''BoltGeometryDatabase: 'BoltGeometryDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1262.BoltGeometryDatabase)(self.wrapped.BoltGeometryDatabase) if self.wrapped.BoltGeometryDatabase is not None else None

    @property
    def bolt_material_database(self) -> '_1264.BoltMaterialDatabase':
        '''BoltMaterialDatabase: 'BoltMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1264.BoltMaterialDatabase)(self.wrapped.BoltMaterialDatabase) if self.wrapped.BoltMaterialDatabase is not None else None

    @property
    def clamped_section_material_database(self) -> '_1269.ClampedSectionMaterialDatabase':
        '''ClampedSectionMaterialDatabase: 'ClampedSectionMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1269.ClampedSectionMaterialDatabase)(self.wrapped.ClampedSectionMaterialDatabase) if self.wrapped.ClampedSectionMaterialDatabase is not None else None

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(self) -> '_875.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_875.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase is not None else None

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(self) -> '_876.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_876.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase is not None else None

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_879.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_879.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(self) -> '_880.ParetoCylindricalGearSetOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetOptimisationStrategyDatabase: 'ParetoCylindricalGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_880.ParetoCylindricalGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_885.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_885.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(self) -> '_886.ParetoHypoidGearSetOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetOptimisationStrategyDatabase: 'ParetoHypoidGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_886.ParetoHypoidGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_888.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_888.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(self) -> '_889.ParetoSpiralBevelGearSetOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_889.ParetoSpiralBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase is not None else None

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_890.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_890.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase is not None else None

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(self) -> '_891.ParetoStraightBevelGearSetOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_891.ParetoStraightBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase is not None else None

    @property
    def manufacturing_machine_database(self) -> '_755.ManufacturingMachineDatabase':
        '''ManufacturingMachineDatabase: 'ManufacturingMachineDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_755.ManufacturingMachineDatabase)(self.wrapped.ManufacturingMachineDatabase) if self.wrapped.ManufacturingMachineDatabase is not None else None

    @property
    def cylindrical_formed_wheel_grinder_database(self) -> '_678.CylindricalFormedWheelGrinderDatabase':
        '''CylindricalFormedWheelGrinderDatabase: 'CylindricalFormedWheelGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_678.CylindricalFormedWheelGrinderDatabase)(self.wrapped.CylindricalFormedWheelGrinderDatabase) if self.wrapped.CylindricalFormedWheelGrinderDatabase is not None else None

    @property
    def cylindrical_gear_plunge_shaver_database(self) -> '_684.CylindricalGearPlungeShaverDatabase':
        '''CylindricalGearPlungeShaverDatabase: 'CylindricalGearPlungeShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_684.CylindricalGearPlungeShaverDatabase)(self.wrapped.CylindricalGearPlungeShaverDatabase) if self.wrapped.CylindricalGearPlungeShaverDatabase is not None else None

    @property
    def cylindrical_gear_shaver_database(self) -> '_689.CylindricalGearShaverDatabase':
        '''CylindricalGearShaverDatabase: 'CylindricalGearShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_689.CylindricalGearShaverDatabase)(self.wrapped.CylindricalGearShaverDatabase) if self.wrapped.CylindricalGearShaverDatabase is not None else None

    @property
    def cylindrical_worm_grinder_database(self) -> '_690.CylindricalWormGrinderDatabase':
        '''CylindricalWormGrinderDatabase: 'CylindricalWormGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_690.CylindricalWormGrinderDatabase)(self.wrapped.CylindricalWormGrinderDatabase) if self.wrapped.CylindricalWormGrinderDatabase is not None else None

    @property
    def cylindrical_hob_database(self) -> '_570.CylindricalHobDatabase':
        '''CylindricalHobDatabase: 'CylindricalHobDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_570.CylindricalHobDatabase)(self.wrapped.CylindricalHobDatabase) if self.wrapped.CylindricalHobDatabase is not None else None

    @property
    def cylindrical_shaper_database(self) -> '_581.CylindricalShaperDatabase':
        '''CylindricalShaperDatabase: 'CylindricalShaperDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_581.CylindricalShaperDatabase)(self.wrapped.CylindricalShaperDatabase) if self.wrapped.CylindricalShaperDatabase is not None else None

    @property
    def bevel_gear_iso_material_database(self) -> '_541.BevelGearIsoMaterialDatabase':
        '''BevelGearIsoMaterialDatabase: 'BevelGearIsoMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_541.BevelGearIsoMaterialDatabase)(self.wrapped.BevelGearIsoMaterialDatabase) if self.wrapped.BevelGearIsoMaterialDatabase is not None else None

    @property
    def bevel_gear_material_database(self) -> '_543.BevelGearMaterialDatabase':
        '''BevelGearMaterialDatabase: 'BevelGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_543.BevelGearMaterialDatabase)(self.wrapped.BevelGearMaterialDatabase) if self.wrapped.BevelGearMaterialDatabase is not None else None

    @property
    def cylindrical_gear_agma_material_database(self) -> '_544.CylindricalGearAGMAMaterialDatabase':
        '''CylindricalGearAGMAMaterialDatabase: 'CylindricalGearAGMAMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_544.CylindricalGearAGMAMaterialDatabase)(self.wrapped.CylindricalGearAGMAMaterialDatabase) if self.wrapped.CylindricalGearAGMAMaterialDatabase is not None else None

    @property
    def cylindrical_gear_iso_material_database(self) -> '_545.CylindricalGearISOMaterialDatabase':
        '''CylindricalGearISOMaterialDatabase: 'CylindricalGearISOMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_545.CylindricalGearISOMaterialDatabase)(self.wrapped.CylindricalGearISOMaterialDatabase) if self.wrapped.CylindricalGearISOMaterialDatabase is not None else None

    @property
    def cylindrical_gear_plastic_material_database(self) -> '_548.CylindricalGearPlasticMaterialDatabase':
        '''CylindricalGearPlasticMaterialDatabase: 'CylindricalGearPlasticMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_548.CylindricalGearPlasticMaterialDatabase)(self.wrapped.CylindricalGearPlasticMaterialDatabase) if self.wrapped.CylindricalGearPlasticMaterialDatabase is not None else None

    @property
    def klingelnberg_conical_gear_material_database(self) -> '_555.KlingelnbergConicalGearMaterialDatabase':
        '''KlingelnbergConicalGearMaterialDatabase: 'KlingelnbergConicalGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_555.KlingelnbergConicalGearMaterialDatabase)(self.wrapped.KlingelnbergConicalGearMaterialDatabase) if self.wrapped.KlingelnbergConicalGearMaterialDatabase is not None else None

    @property
    def raw_material_database(self) -> '_562.RawMaterialDatabase':
        '''RawMaterialDatabase: 'RawMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_562.RawMaterialDatabase)(self.wrapped.RawMaterialDatabase) if self.wrapped.RawMaterialDatabase is not None else None

    @property
    def conical_gear_optimization_strategy_database(self) -> '_1958.ConicalGearOptimizationStrategyDatabase':
        '''ConicalGearOptimizationStrategyDatabase: 'ConicalGearOptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1958.ConicalGearOptimizationStrategyDatabase)(self.wrapped.ConicalGearOptimizationStrategyDatabase) if self.wrapped.ConicalGearOptimizationStrategyDatabase is not None else None

    @property
    def optimization_strategy_database(self) -> '_1967.OptimizationStrategyDatabase':
        '''OptimizationStrategyDatabase: 'OptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.OptimizationStrategyDatabase)(self.wrapped.OptimizationStrategyDatabase) if self.wrapped.OptimizationStrategyDatabase is not None else None

    @property
    def supercharger_rotor_set_database(self) -> '_2289.SuperchargerRotorSetDatabase':
        '''SuperchargerRotorSetDatabase: 'SuperchargerRotorSetDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.SuperchargerRotorSetDatabase)(self.wrapped.SuperchargerRotorSetDatabase) if self.wrapped.SuperchargerRotorSetDatabase is not None else None

    @property
    def bearing_material_database(self) -> '_218.BearingMaterialDatabase':
        '''BearingMaterialDatabase: 'BearingMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_218.BearingMaterialDatabase)(self.wrapped.BearingMaterialDatabase) if self.wrapped.BearingMaterialDatabase is not None else None

    @property
    def component_material_database(self) -> '_219.ComponentMaterialDatabase':
        '''ComponentMaterialDatabase: 'ComponentMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_219.ComponentMaterialDatabase)(self.wrapped.ComponentMaterialDatabase) if self.wrapped.ComponentMaterialDatabase is not None else None

    @property
    def lubrication_detail_database(self) -> '_238.LubricationDetailDatabase':
        '''LubricationDetailDatabase: 'LubricationDetailDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_238.LubricationDetailDatabase)(self.wrapped.LubricationDetailDatabase) if self.wrapped.LubricationDetailDatabase is not None else None

    @property
    def shaft_material_database(self) -> '_25.ShaftMaterialDatabase':
        '''ShaftMaterialDatabase: 'ShaftMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_25.ShaftMaterialDatabase)(self.wrapped.ShaftMaterialDatabase) if self.wrapped.ShaftMaterialDatabase is not None else None
