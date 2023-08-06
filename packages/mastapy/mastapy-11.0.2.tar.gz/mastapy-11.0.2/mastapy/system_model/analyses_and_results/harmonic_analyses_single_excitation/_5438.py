'''_5438.py

SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6600
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5436, _5437, _5354
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation',)


class SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation(_5354.BevelGearSetHarmonicAnalysisOfSingleExcitation):
    '''SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2221.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6600.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6600.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def spiral_bevel_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5436.SpiralBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearHarmonicAnalysisOfSingleExcitation]: 'SpiralBevelGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5436.SpiralBevelGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def spiral_bevel_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5437.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]: 'SpiralBevelMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5437.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
