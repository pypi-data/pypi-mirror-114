'''_6799.py

BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6797, _6798, _6804
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6669
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6804.BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6797.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6797.BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6798.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6798.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6669.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
