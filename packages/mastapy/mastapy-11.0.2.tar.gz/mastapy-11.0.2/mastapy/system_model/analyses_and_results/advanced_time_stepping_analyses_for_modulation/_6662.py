'''_6662.py

AssemblyAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2114, _2153
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6460, _6592
from mastapy.system_model.analyses_and_results.system_deflections import _2367, _2468
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _6664, _6666, _6669, _6675,
    _6676, _6677, _6682, _6687,
    _6696, _6699, _6700, _6705,
    _6711, _6712, _6713, _6721,
    _6728, _6731, _6732, _6733,
    _6735, _6737, _6742, _6743,
    _6744, _6753, _6746, _6749,
    _6752, _6758, _6759, _6764,
    _6767, _6770, _6774, _6778,
    _6782, _6785, _6652
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'AssemblyAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedTimeSteppingAnalysisForModulation',)


class AssemblyAdvancedTimeSteppingAnalysisForModulation(_6652.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation):
    '''AssemblyAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6460.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6460.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2367.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2367.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def bearings(self) -> 'List[_6664.BearingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BearingAdvancedTimeSteppingAnalysisForModulation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6664.BearingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def belt_drives(self) -> 'List[_6666.BeltDriveAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BeltDriveAdvancedTimeSteppingAnalysisForModulation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6666.BeltDriveAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolts(self) -> 'List[_6675.BoltAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltAdvancedTimeSteppingAnalysisForModulation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6675.BoltAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolted_joints(self) -> 'List[_6676.BoltedJointAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltedJointAdvancedTimeSteppingAnalysisForModulation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6676.BoltedJointAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def clutches(self) -> 'List[_6677.ClutchAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchAdvancedTimeSteppingAnalysisForModulation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6677.ClutchAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_couplings(self) -> 'List[_6682.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6682.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6687.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6687.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cv_ts(self) -> 'List[_6696.CVTAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CVTAdvancedTimeSteppingAnalysisForModulation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6696.CVTAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6699.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6699.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6700.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6700.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6705.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6705.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6711.FaceGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6711.FaceGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def fe_parts(self) -> 'List[_6712.FEPartAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FEPartAdvancedTimeSteppingAnalysisForModulation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6712.FEPartAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6713.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6713.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6721.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6721.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6728.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6728.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6731.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6731.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def mass_discs(self) -> 'List[_6732.MassDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MassDiscAdvancedTimeSteppingAnalysisForModulation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6732.MassDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def measurement_components(self) -> 'List[_6733.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6733.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def oil_seals(self) -> 'List[_6735.OilSealAdvancedTimeSteppingAnalysisForModulation]':
        '''List[OilSealAdvancedTimeSteppingAnalysisForModulation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6735.OilSealAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6737.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6737.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def planet_carriers(self) -> 'List[_6742.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6742.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def point_loads(self) -> 'List[_6743.PointLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PointLoadAdvancedTimeSteppingAnalysisForModulation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6743.PointLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def power_loads(self) -> 'List[_6744.PowerLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PowerLoadAdvancedTimeSteppingAnalysisForModulation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6744.PowerLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6753.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6753.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def ring_pins(self) -> 'List[_6746.RingPinsAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RingPinsAdvancedTimeSteppingAnalysisForModulation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6746.RingPinsAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6749.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6749.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shafts(self) -> 'List[_6752.ShaftAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftAdvancedTimeSteppingAnalysisForModulation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6752.ShaftAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6758.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6758.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spring_dampers(self) -> 'List[_6759.SpringDamperAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperAdvancedTimeSteppingAnalysisForModulation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6759.SpringDamperAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6764.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6764.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6767.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6767.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def synchronisers(self) -> 'List[_6770.SynchroniserAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SynchroniserAdvancedTimeSteppingAnalysisForModulation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6770.SynchroniserAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def torque_converters(self) -> 'List[_6774.TorqueConverterAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterAdvancedTimeSteppingAnalysisForModulation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6774.TorqueConverterAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6778.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]':
        '''List[UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6778.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6782.WormGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[WormGearSetAdvancedTimeSteppingAnalysisForModulation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6782.WormGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6785.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6785.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
