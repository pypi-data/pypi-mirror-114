'''_735.py

ConicalMeshMicroGeometryConfigBase
'''


from mastapy.gears.manufacturing.bevel import (
    _726, _724, _725, _736,
    _737, _742
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.conical import _1068
from mastapy.gears.gear_designs.zerol_bevel import _884
from mastapy.gears.gear_designs.straight_bevel_diff import _893
from mastapy.gears.gear_designs.straight_bevel import _897
from mastapy.gears.gear_designs.spiral_bevel import _901
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _905
from mastapy.gears.gear_designs.klingelnberg_hypoid import _909
from mastapy.gears.gear_designs.klingelnberg_conical import _913
from mastapy.gears.gear_designs.hypoid import _917
from mastapy.gears.gear_designs.bevel import _1094
from mastapy.gears.gear_designs.agma_gleason_conical import _1107
from mastapy.gears.analysis import _1135
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshMicroGeometryConfigBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMicroGeometryConfigBase',)


class ConicalMeshMicroGeometryConfigBase(_1135.GearMeshImplementationDetail):
    '''ConicalMeshMicroGeometryConfigBase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshMicroGeometryConfigBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_config(self) -> '_726.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_manufacturing_config(self) -> '_724.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.ConicalGearManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_micro_geometry_config(self) -> '_725.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _725.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_manufacturing_config(self) -> '_736.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_micro_geometry_config(self) -> '_737.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _737.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_wheel_manufacturing_config(self) -> '_742.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _742.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def mesh(self) -> '_1068.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1068.ConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_zerol_bevel_gear_mesh_design(self) -> '_884.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _884.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_893.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _893.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_gear_mesh_design(self) -> '_897.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _897.StraightBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_spiral_bevel_gear_mesh_design(self) -> '_901.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _901.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_905.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _905.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_909.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _909.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_913.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_hypoid_gear_mesh_design(self) -> '_917.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.HypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_bevel_gear_mesh_design(self) -> '_1094.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1094.BevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_1107.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1107.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None
