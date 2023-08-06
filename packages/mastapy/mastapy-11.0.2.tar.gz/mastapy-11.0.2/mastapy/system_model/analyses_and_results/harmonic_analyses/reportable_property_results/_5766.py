'''_5766.py

FEPartHarmonicAnalysisResultsPropertyAccessor
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5767, _5777, _5773
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_FE_PART_HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'FEPartHarmonicAnalysisResultsPropertyAccessor')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartHarmonicAnalysisResultsPropertyAccessor',)


class FEPartHarmonicAnalysisResultsPropertyAccessor(_5773.HarmonicAnalysisResultsPropertyAccessor):
    '''FEPartHarmonicAnalysisResultsPropertyAccessor

    This is a mastapy class.
    '''

    TYPE = _FE_PART_HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartHarmonicAnalysisResultsPropertyAccessor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excitations(self) -> 'List[_5767.FEPartSingleWhineAnalysisResultsPropertyAccessor]':
        '''List[FEPartSingleWhineAnalysisResultsPropertyAccessor]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Excitations, constructor.new(_5767.FEPartSingleWhineAnalysisResultsPropertyAccessor))
        return value

    @property
    def orders_for_combined_excitations(self) -> 'List[_5777.ResultsForOrderIncludingSurfaces]':
        '''List[ResultsForOrderIncludingSurfaces]: 'OrdersForCombinedExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OrdersForCombinedExcitations, constructor.new(_5777.ResultsForOrderIncludingSurfaces))
        return value
