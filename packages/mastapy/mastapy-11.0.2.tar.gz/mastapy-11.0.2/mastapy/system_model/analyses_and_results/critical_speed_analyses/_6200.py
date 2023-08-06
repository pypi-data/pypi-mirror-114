'''_6200.py

BevelDifferentialGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6466
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6198, _6199, _6205
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BevelDifferentialGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCriticalSpeedAnalysis',)


class BevelDifferentialGearSetCriticalSpeedAnalysis(_6205.BevelGearSetCriticalSpeedAnalysis):
    '''BevelDifferentialGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6466.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6466.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_critical_speed_analysis(self) -> 'List[_6198.BevelDifferentialGearCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearCriticalSpeedAnalysis]: 'BevelDifferentialGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCriticalSpeedAnalysis, constructor.new(_6198.BevelDifferentialGearCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_meshes_critical_speed_analysis(self) -> 'List[_6199.BevelDifferentialGearMeshCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearMeshCriticalSpeedAnalysis]: 'BevelDifferentialMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCriticalSpeedAnalysis, constructor.new(_6199.BevelDifferentialGearMeshCriticalSpeedAnalysis))
        return value
