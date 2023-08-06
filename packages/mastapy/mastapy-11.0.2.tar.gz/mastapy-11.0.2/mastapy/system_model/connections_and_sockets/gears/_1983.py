'''_1983.py

BevelDifferentialGearMesh
'''


from mastapy.gears.gear_designs.bevel import _1094
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _884
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _893
from mastapy.gears.gear_designs.straight_bevel import _897
from mastapy.gears.gear_designs.spiral_bevel import _901
from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMesh',)


class BevelDifferentialGearMesh(_1985.BevelGearMesh):
    '''BevelDifferentialGearMesh

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_1094.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1094.BevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_884.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _884.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_893.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _893.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_897.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _897.StraightBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def bevel_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_901.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _901.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.BevelGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.BevelGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMeshDesign.__class__)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None
