'''_6687.py

ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6484
from mastapy.system_model.analyses_and_results.system_deflections import _2391
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6685, _6686, _6716
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'ConceptGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetAdvancedTimeSteppingAnalysisForModulation',)


class ConceptGearSetAdvancedTimeSteppingAnalysisForModulation(_6716.GearSetAdvancedTimeSteppingAnalysisForModulation):
    '''ConceptGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2199.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2199.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6484.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6484.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2391.ConceptGearSetSystemDeflection':
        '''ConceptGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2391.ConceptGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def concept_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6685.ConceptGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6685.ConceptGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6686.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'ConceptMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6686.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
