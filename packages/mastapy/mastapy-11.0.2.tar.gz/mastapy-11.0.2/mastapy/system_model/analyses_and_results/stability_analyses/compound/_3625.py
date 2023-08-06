'''_3625.py

HypoidGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2211
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3496
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3567
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'HypoidGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundStabilityAnalysis',)


class HypoidGearCompoundStabilityAnalysis(_3567.AGMAGleasonConicalGearCompoundStabilityAnalysis):
    '''HypoidGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2211.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2211.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3496.HypoidGearStabilityAnalysis]':
        '''List[HypoidGearStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3496.HypoidGearStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3496.HypoidGearStabilityAnalysis]':
        '''List[HypoidGearStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3496.HypoidGearStabilityAnalysis))
        return value
