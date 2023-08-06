'''_3718.py

BoltPowerFlow
'''


from mastapy.system_model.part_model import _2122
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6473
from mastapy.system_model.analyses_and_results.power_flows import _3723
from mastapy._internal.python_net import python_net_import

_BOLT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BoltPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltPowerFlow',)


class BoltPowerFlow(_3723.ComponentPowerFlow):
    '''BoltPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLT_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltPowerFlow.TYPE'):
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
    def component_load_case(self) -> '_6473.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6473.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
