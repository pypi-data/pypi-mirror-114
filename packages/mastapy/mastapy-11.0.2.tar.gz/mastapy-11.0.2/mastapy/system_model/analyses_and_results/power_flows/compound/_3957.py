'''_3957.py

ZerolBevelGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2230
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3829
from mastapy.system_model.analyses_and_results.power_flows.compound import _3847
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ZerolBevelGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearCompoundPowerFlow',)


class ZerolBevelGearCompoundPowerFlow(_3847.BevelGearCompoundPowerFlow):
    '''ZerolBevelGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2230.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2230.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3829.ZerolBevelGearPowerFlow]':
        '''List[ZerolBevelGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3829.ZerolBevelGearPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3829.ZerolBevelGearPowerFlow]':
        '''List[ZerolBevelGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3829.ZerolBevelGearPowerFlow))
        return value
