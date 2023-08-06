'''_3908.py

MountableComponentCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.analyses_and_results.power_flows import _3776
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3856
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'MountableComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundPowerFlow',)


class MountableComponentCompoundPowerFlow(_3856.ComponentCompoundPowerFlow):
    '''MountableComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_3776.MountableComponentPowerFlow]':
        '''List[MountableComponentPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3776.MountableComponentPowerFlow))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3776.MountableComponentPowerFlow]':
        '''List[MountableComponentPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3776.MountableComponentPowerFlow))
        return value
