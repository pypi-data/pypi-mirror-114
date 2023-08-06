'''_684.py

InvoluteCutterDesign
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _295
from mastapy.gears.gear_designs.cylindrical import (
    _1012, _973, _994, _1011
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _679
from mastapy._internal.python_net import python_net_import

_INVOLUTE_CUTTER_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'InvoluteCutterDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('InvoluteCutterDesign',)


class InvoluteCutterDesign(_679.CylindricalGearRealCutterDesign):
    '''InvoluteCutterDesign

    This is a mastapy class.
    '''

    TYPE = _INVOLUTE_CUTTER_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InvoluteCutterDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_teeth(self) -> 'float':
        '''float: 'NumberOfTeeth' is the original name of this property.'''

        return self.wrapped.NumberOfTeeth

    @number_of_teeth.setter
    def number_of_teeth(self, value: 'float'):
        self.wrapped.NumberOfTeeth = float(value) if value else 0.0

    @property
    def hand(self) -> '_295.Hand':
        '''Hand: 'Hand' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Hand)
        return constructor.new(_295.Hand)(value) if value else None

    @hand.setter
    def hand(self, value: '_295.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def tooth_thickness(self) -> '_1012.ToothThicknessSpecificationBase':
        '''ToothThicknessSpecificationBase: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1012.ToothThicknessSpecificationBase.TYPE not in self.wrapped.ToothThickness.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ToothThicknessSpecificationBase. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThickness.__class__)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None

    @property
    def tooth_thickness_of_type_finish_tooth_thickness_design_specification(self) -> '_973.FinishToothThicknessDesignSpecification':
        '''FinishToothThicknessDesignSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _973.FinishToothThicknessDesignSpecification.TYPE not in self.wrapped.ToothThickness.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to FinishToothThicknessDesignSpecification. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThickness.__class__)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None

    @property
    def tooth_thickness_of_type_readonly_tooth_thickness_specification(self) -> '_994.ReadonlyToothThicknessSpecification':
        '''ReadonlyToothThicknessSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _994.ReadonlyToothThicknessSpecification.TYPE not in self.wrapped.ToothThickness.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ReadonlyToothThicknessSpecification. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThickness.__class__)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None

    @property
    def tooth_thickness_of_type_tooth_thickness_specification(self) -> '_1011.ToothThicknessSpecification':
        '''ToothThicknessSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1011.ToothThicknessSpecification.TYPE not in self.wrapped.ToothThickness.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness to ToothThicknessSpecification. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThickness.__class__)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None
