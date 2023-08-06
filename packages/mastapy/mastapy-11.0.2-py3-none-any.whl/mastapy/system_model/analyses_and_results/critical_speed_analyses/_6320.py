'''_6320.py

ZerolBevelGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2230
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6637
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6318, _6319, _6208
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ZerolBevelGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCriticalSpeedAnalysis',)


class ZerolBevelGearSetCriticalSpeedAnalysis(_6208.BevelGearSetCriticalSpeedAnalysis):
    '''ZerolBevelGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2230.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2230.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6637.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6637.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_critical_speed_analysis(self) -> 'List[_6318.ZerolBevelGearCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearCriticalSpeedAnalysis]: 'ZerolBevelGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCriticalSpeedAnalysis, constructor.new(_6318.ZerolBevelGearCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_meshes_critical_speed_analysis(self) -> 'List[_6319.ZerolBevelGearMeshCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearMeshCriticalSpeedAnalysis]: 'ZerolBevelMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCriticalSpeedAnalysis, constructor.new(_6319.ZerolBevelGearMeshCriticalSpeedAnalysis))
        return value
