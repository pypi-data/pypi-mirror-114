'''_3921.py

RingPinsToDiscConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2023
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3791
from mastapy.system_model.analyses_and_results.power_flows.compound import _3896
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RingPinsToDiscConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundPowerFlow',)


class RingPinsToDiscConnectionCompoundPowerFlow(_3896.InterMountableComponentConnectionCompoundPowerFlow):
    '''RingPinsToDiscConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2023.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2023.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2023.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2023.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3791.RingPinsToDiscConnectionPowerFlow]':
        '''List[RingPinsToDiscConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3791.RingPinsToDiscConnectionPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3791.RingPinsToDiscConnectionPowerFlow]':
        '''List[RingPinsToDiscConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3791.RingPinsToDiscConnectionPowerFlow))
        return value
