'''_2462.py

RingPinsSystemDeflection
'''


from mastapy.system_model.part_model.cycloidal import _2247
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6587
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy.system_model.analyses_and_results.system_deflections import _2450
from mastapy._internal.python_net import python_net_import

_RING_PINS_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RingPinsSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsSystemDeflection',)


class RingPinsSystemDeflection(_2450.MountableComponentSystemDeflection):
    '''RingPinsSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2247.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2247.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6587.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6587.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3790.RingPinsPowerFlow':
        '''RingPinsPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3790.RingPinsPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
