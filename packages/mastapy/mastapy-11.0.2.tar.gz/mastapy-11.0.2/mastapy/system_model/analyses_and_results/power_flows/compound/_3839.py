'''_3839.py

BearingCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3706
from mastapy.system_model.analyses_and_results.power_flows.compound import _3867
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BearingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundPowerFlow',)


class BearingCompoundPowerFlow(_3867.ConnectorCompoundPowerFlow):
    '''BearingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3706.BearingPowerFlow]':
        '''List[BearingPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3706.BearingPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3706.BearingPowerFlow]':
        '''List[BearingPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3706.BearingPowerFlow))
        return value
