'''_3624.py

GuideDxfModelCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3493
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3588
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'GuideDxfModelCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundStabilityAnalysis',)


class GuideDxfModelCompoundStabilityAnalysis(_3588.ComponentCompoundStabilityAnalysis):
    '''GuideDxfModelCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2134.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3493.GuideDxfModelStabilityAnalysis]':
        '''List[GuideDxfModelStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3493.GuideDxfModelStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3493.GuideDxfModelStabilityAnalysis]':
        '''List[GuideDxfModelStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3493.GuideDxfModelStabilityAnalysis))
        return value
