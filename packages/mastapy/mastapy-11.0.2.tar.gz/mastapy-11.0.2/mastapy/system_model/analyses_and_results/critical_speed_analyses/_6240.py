'''_6240.py

DatumCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6510
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6212
from mastapy._internal.python_net import python_net_import

_DATUM_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'DatumCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCriticalSpeedAnalysis',)


class DatumCriticalSpeedAnalysis(_6212.ComponentCriticalSpeedAnalysis):
    '''DatumCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6510.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6510.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
