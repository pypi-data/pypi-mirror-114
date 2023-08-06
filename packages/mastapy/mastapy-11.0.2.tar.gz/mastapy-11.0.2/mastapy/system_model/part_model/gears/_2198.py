'''_2198.py

ConceptGear
'''


from mastapy.system_model.part_model.gears import _2208, _2207
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.concept import _1089
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGear',)


class ConceptGear(_2207.Gear):
    '''ConceptGear

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def orientation(self) -> '_2208.GearOrientations':
        '''GearOrientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_2208.GearOrientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_2208.GearOrientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def active_gear_design(self) -> '_1089.ConceptGearDesign':
        '''ConceptGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1089.ConceptGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def concept_gear_design(self) -> '_1089.ConceptGearDesign':
        '''ConceptGearDesign: 'ConceptGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1089.ConceptGearDesign)(self.wrapped.ConceptGearDesign) if self.wrapped.ConceptGearDesign else None
