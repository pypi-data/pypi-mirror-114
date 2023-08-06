'''_6130.py

OilSealCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6001
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6088
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'OilSealCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundDynamicAnalysis',)


class OilSealCompoundDynamicAnalysis(_6088.ConnectorCompoundDynamicAnalysis):
    '''OilSealCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6001.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6001.OilSealDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6001.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6001.OilSealDynamicAnalysis))
        return value
