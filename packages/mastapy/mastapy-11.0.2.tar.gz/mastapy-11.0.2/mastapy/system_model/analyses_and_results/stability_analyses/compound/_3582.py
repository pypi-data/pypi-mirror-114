'''_3582.py

BoltCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3451
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3588
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'BoltCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundStabilityAnalysis',)


class BoltCompoundStabilityAnalysis(_3588.ComponentCompoundStabilityAnalysis):
    '''BoltCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2122.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3451.BoltStabilityAnalysis]':
        '''List[BoltStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3451.BoltStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3451.BoltStabilityAnalysis]':
        '''List[BoltStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3451.BoltStabilityAnalysis))
        return value
