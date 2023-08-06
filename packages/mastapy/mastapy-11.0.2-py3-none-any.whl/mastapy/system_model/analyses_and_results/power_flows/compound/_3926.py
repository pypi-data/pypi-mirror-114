'''_3926.py

ShaftCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2160
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3797
from mastapy.system_model.analyses_and_results.power_flows.compound import _3832
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ShaftCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundPowerFlow',)


class ShaftCompoundPowerFlow(_3832.AbstractShaftCompoundPowerFlow):
    '''ShaftCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2160.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2160.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3797.ShaftPowerFlow]':
        '''List[ShaftPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3797.ShaftPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3797.ShaftPowerFlow]':
        '''List[ShaftPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3797.ShaftPowerFlow))
        return value
