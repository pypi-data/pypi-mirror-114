'''_5949.py

ConceptCouplingDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2258
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6481
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5960
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptCouplingDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingDynamicAnalysis',)


class ConceptCouplingDynamicAnalysis(_5960.CouplingDynamicAnalysis):
    '''ConceptCouplingDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2258.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2258.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6481.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6481.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
