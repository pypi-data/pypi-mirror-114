'''_4088.py

StraightBevelGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6610
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4087, _4086, _3978
from mastapy.system_model.analyses_and_results.system_deflections import _2485
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'StraightBevelGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetParametricStudyTool',)


class StraightBevelGearSetParametricStudyTool(_3978.BevelGearSetParametricStudyTool):
    '''StraightBevelGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2225.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6610.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6610.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_parametric_study_tool(self) -> 'List[_4087.StraightBevelGearParametricStudyTool]':
        '''List[StraightBevelGearParametricStudyTool]: 'StraightBevelGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsParametricStudyTool, constructor.new(_4087.StraightBevelGearParametricStudyTool))
        return value

    @property
    def straight_bevel_meshes_parametric_study_tool(self) -> 'List[_4086.StraightBevelGearMeshParametricStudyTool]':
        '''List[StraightBevelGearMeshParametricStudyTool]: 'StraightBevelMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesParametricStudyTool, constructor.new(_4086.StraightBevelGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2485.StraightBevelGearSetSystemDeflection]':
        '''List[StraightBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2485.StraightBevelGearSetSystemDeflection))
        return value
