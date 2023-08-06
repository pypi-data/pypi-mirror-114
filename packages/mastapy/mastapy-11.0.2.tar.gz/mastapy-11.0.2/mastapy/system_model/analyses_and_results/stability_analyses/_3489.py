'''_3489.py

FlexiblePinAssemblyStabilityAnalysis
'''


from mastapy.system_model.part_model import _2133
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6530
from mastapy.system_model.analyses_and_results.stability_analyses import _3530
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'FlexiblePinAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyStabilityAnalysis',)


class FlexiblePinAssemblyStabilityAnalysis(_3530.SpecialisedAssemblyStabilityAnalysis):
    '''FlexiblePinAssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2133.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6530.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6530.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
