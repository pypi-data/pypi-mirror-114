'''_3838.py

AssemblyCompoundPowerFlow
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2114, _2153
from mastapy._internal.cast_exception import CastException
from mastapy.gears.analysis import _1137
from mastapy.system_model.analyses_and_results.power_flows import _3705
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3839, _3841, _3844, _3850,
    _3851, _3852, _3857, _3862,
    _3872, _3874, _3876, _3880,
    _3886, _3887, _3888, _3895,
    _3902, _3905, _3906, _3907,
    _3909, _3911, _3916, _3917,
    _3918, _3927, _3920, _3922,
    _3926, _3932, _3933, _3938,
    _3941, _3944, _3948, _3952,
    _3956, _3959, _3831
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundPowerFlow',)


class AssemblyCompoundPowerFlow(_3831.AbstractAssemblyCompoundPowerFlow):
    '''AssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def input_power_load_ratio_warning(self) -> 'str':
        '''str: 'InputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InputPowerLoadRatioWarning

    @property
    def output_power_load_ratio_warning(self) -> 'str':
        '''str: 'OutputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OutputPowerLoadRatioWarning

    @property
    def component_design(self) -> '_2114.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2114.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def rating_for_all_gear_sets(self) -> '_1137.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1137.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3705.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3705.AssemblyPowerFlow))
        return value

    @property
    def bearings(self) -> 'List[_3839.BearingCompoundPowerFlow]':
        '''List[BearingCompoundPowerFlow]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3839.BearingCompoundPowerFlow))
        return value

    @property
    def belt_drives(self) -> 'List[_3841.BeltDriveCompoundPowerFlow]':
        '''List[BeltDriveCompoundPowerFlow]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3841.BeltDriveCompoundPowerFlow))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3844.BevelDifferentialGearSetCompoundPowerFlow]':
        '''List[BevelDifferentialGearSetCompoundPowerFlow]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3844.BevelDifferentialGearSetCompoundPowerFlow))
        return value

    @property
    def bolts(self) -> 'List[_3850.BoltCompoundPowerFlow]':
        '''List[BoltCompoundPowerFlow]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3850.BoltCompoundPowerFlow))
        return value

    @property
    def bolted_joints(self) -> 'List[_3851.BoltedJointCompoundPowerFlow]':
        '''List[BoltedJointCompoundPowerFlow]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3851.BoltedJointCompoundPowerFlow))
        return value

    @property
    def clutches(self) -> 'List[_3852.ClutchCompoundPowerFlow]':
        '''List[ClutchCompoundPowerFlow]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3852.ClutchCompoundPowerFlow))
        return value

    @property
    def concept_couplings(self) -> 'List[_3857.ConceptCouplingCompoundPowerFlow]':
        '''List[ConceptCouplingCompoundPowerFlow]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3857.ConceptCouplingCompoundPowerFlow))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3862.ConceptGearSetCompoundPowerFlow]':
        '''List[ConceptGearSetCompoundPowerFlow]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3862.ConceptGearSetCompoundPowerFlow))
        return value

    @property
    def cv_ts(self) -> 'List[_3872.CVTCompoundPowerFlow]':
        '''List[CVTCompoundPowerFlow]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3872.CVTCompoundPowerFlow))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3874.CycloidalAssemblyCompoundPowerFlow]':
        '''List[CycloidalAssemblyCompoundPowerFlow]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3874.CycloidalAssemblyCompoundPowerFlow))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3876.CycloidalDiscCompoundPowerFlow]':
        '''List[CycloidalDiscCompoundPowerFlow]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3876.CycloidalDiscCompoundPowerFlow))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3880.CylindricalGearSetCompoundPowerFlow]':
        '''List[CylindricalGearSetCompoundPowerFlow]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3880.CylindricalGearSetCompoundPowerFlow))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3886.FaceGearSetCompoundPowerFlow]':
        '''List[FaceGearSetCompoundPowerFlow]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3886.FaceGearSetCompoundPowerFlow))
        return value

    @property
    def fe_parts(self) -> 'List[_3887.FEPartCompoundPowerFlow]':
        '''List[FEPartCompoundPowerFlow]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3887.FEPartCompoundPowerFlow))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3888.FlexiblePinAssemblyCompoundPowerFlow]':
        '''List[FlexiblePinAssemblyCompoundPowerFlow]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3888.FlexiblePinAssemblyCompoundPowerFlow))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3895.HypoidGearSetCompoundPowerFlow]':
        '''List[HypoidGearSetCompoundPowerFlow]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3895.HypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3902.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3902.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3905.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3905.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def mass_discs(self) -> 'List[_3906.MassDiscCompoundPowerFlow]':
        '''List[MassDiscCompoundPowerFlow]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3906.MassDiscCompoundPowerFlow))
        return value

    @property
    def measurement_components(self) -> 'List[_3907.MeasurementComponentCompoundPowerFlow]':
        '''List[MeasurementComponentCompoundPowerFlow]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3907.MeasurementComponentCompoundPowerFlow))
        return value

    @property
    def oil_seals(self) -> 'List[_3909.OilSealCompoundPowerFlow]':
        '''List[OilSealCompoundPowerFlow]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3909.OilSealCompoundPowerFlow))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3911.PartToPartShearCouplingCompoundPowerFlow]':
        '''List[PartToPartShearCouplingCompoundPowerFlow]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3911.PartToPartShearCouplingCompoundPowerFlow))
        return value

    @property
    def planet_carriers(self) -> 'List[_3916.PlanetCarrierCompoundPowerFlow]':
        '''List[PlanetCarrierCompoundPowerFlow]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3916.PlanetCarrierCompoundPowerFlow))
        return value

    @property
    def point_loads(self) -> 'List[_3917.PointLoadCompoundPowerFlow]':
        '''List[PointLoadCompoundPowerFlow]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3917.PointLoadCompoundPowerFlow))
        return value

    @property
    def power_loads(self) -> 'List[_3918.PowerLoadCompoundPowerFlow]':
        '''List[PowerLoadCompoundPowerFlow]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3918.PowerLoadCompoundPowerFlow))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3927.ShaftHubConnectionCompoundPowerFlow]':
        '''List[ShaftHubConnectionCompoundPowerFlow]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3927.ShaftHubConnectionCompoundPowerFlow))
        return value

    @property
    def ring_pins(self) -> 'List[_3920.RingPinsCompoundPowerFlow]':
        '''List[RingPinsCompoundPowerFlow]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3920.RingPinsCompoundPowerFlow))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3922.RollingRingAssemblyCompoundPowerFlow]':
        '''List[RollingRingAssemblyCompoundPowerFlow]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3922.RollingRingAssemblyCompoundPowerFlow))
        return value

    @property
    def shafts(self) -> 'List[_3926.ShaftCompoundPowerFlow]':
        '''List[ShaftCompoundPowerFlow]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3926.ShaftCompoundPowerFlow))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3932.SpiralBevelGearSetCompoundPowerFlow]':
        '''List[SpiralBevelGearSetCompoundPowerFlow]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3932.SpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def spring_dampers(self) -> 'List[_3933.SpringDamperCompoundPowerFlow]':
        '''List[SpringDamperCompoundPowerFlow]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3933.SpringDamperCompoundPowerFlow))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3938.StraightBevelDiffGearSetCompoundPowerFlow]':
        '''List[StraightBevelDiffGearSetCompoundPowerFlow]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3938.StraightBevelDiffGearSetCompoundPowerFlow))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3941.StraightBevelGearSetCompoundPowerFlow]':
        '''List[StraightBevelGearSetCompoundPowerFlow]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3941.StraightBevelGearSetCompoundPowerFlow))
        return value

    @property
    def synchronisers(self) -> 'List[_3944.SynchroniserCompoundPowerFlow]':
        '''List[SynchroniserCompoundPowerFlow]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3944.SynchroniserCompoundPowerFlow))
        return value

    @property
    def torque_converters(self) -> 'List[_3948.TorqueConverterCompoundPowerFlow]':
        '''List[TorqueConverterCompoundPowerFlow]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3948.TorqueConverterCompoundPowerFlow))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3952.UnbalancedMassCompoundPowerFlow]':
        '''List[UnbalancedMassCompoundPowerFlow]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3952.UnbalancedMassCompoundPowerFlow))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3956.WormGearSetCompoundPowerFlow]':
        '''List[WormGearSetCompoundPowerFlow]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3956.WormGearSetCompoundPowerFlow))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3959.ZerolBevelGearSetCompoundPowerFlow]':
        '''List[ZerolBevelGearSetCompoundPowerFlow]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3959.ZerolBevelGearSetCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3705.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3705.AssemblyPowerFlow))
        return value
