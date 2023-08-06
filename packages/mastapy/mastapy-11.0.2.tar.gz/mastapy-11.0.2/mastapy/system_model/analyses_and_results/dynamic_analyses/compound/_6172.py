'''_6172.py

TorqueConverterTurbineCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2287
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6043
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6091
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'TorqueConverterTurbineCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundDynamicAnalysis',)


class TorqueConverterTurbineCompoundDynamicAnalysis(_6091.CouplingHalfCompoundDynamicAnalysis):
    '''TorqueConverterTurbineCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2287.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2287.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6043.TorqueConverterTurbineDynamicAnalysis]':
        '''List[TorqueConverterTurbineDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6043.TorqueConverterTurbineDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6043.TorqueConverterTurbineDynamicAnalysis]':
        '''List[TorqueConverterTurbineDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6043.TorqueConverterTurbineDynamicAnalysis))
        return value
