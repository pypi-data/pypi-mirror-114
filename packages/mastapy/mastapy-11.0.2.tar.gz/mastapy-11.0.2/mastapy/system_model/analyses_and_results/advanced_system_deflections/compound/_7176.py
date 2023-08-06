'''_7176.py

WormGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.rating.worm import _337
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2229
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7174, _7175, _7111
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7047
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'WormGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundAdvancedSystemDeflection',)


class WormGearSetCompoundAdvancedSystemDeflection(_7111.GearSetCompoundAdvancedSystemDeflection):
    '''WormGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_337.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_337.WormGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def worm_gear_duty_cycle_rating(self) -> '_337.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'WormGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_337.WormGearSetDutyCycleRating)(self.wrapped.WormGearDutyCycleRating) if self.wrapped.WormGearDutyCycleRating else None

    @property
    def component_design(self) -> '_2229.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2229.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_advanced_system_deflection(self) -> 'List[_7174.WormGearCompoundAdvancedSystemDeflection]':
        '''List[WormGearCompoundAdvancedSystemDeflection]: 'WormGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundAdvancedSystemDeflection, constructor.new(_7174.WormGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def worm_meshes_compound_advanced_system_deflection(self) -> 'List[_7175.WormGearMeshCompoundAdvancedSystemDeflection]':
        '''List[WormGearMeshCompoundAdvancedSystemDeflection]: 'WormMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundAdvancedSystemDeflection, constructor.new(_7175.WormGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7047.WormGearSetAdvancedSystemDeflection]':
        '''List[WormGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_7047.WormGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_7047.WormGearSetAdvancedSystemDeflection]':
        '''List[WormGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_7047.WormGearSetAdvancedSystemDeflection))
        return value
