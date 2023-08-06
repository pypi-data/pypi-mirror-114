'''_3720.py

ClutchHalfPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2256
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6475
from mastapy.system_model.analyses_and_results.power_flows import _3736
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ClutchHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfPowerFlow',)


class ClutchHalfPowerFlow(_3736.CouplingHalfPowerFlow):
    '''ClutchHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2256.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6475.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6475.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
