'''_1573.py

MASTAGUI
'''


from typing import List, Dict

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.system_model import _1893, _1889
from mastapy.system_model.connections_and_sockets import (
    _1947, _1950, _1951, _1954,
    _1955, _1963, _1969, _1974,
    _1977
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1981, _1983, _1985, _1987,
    _1989, _1991, _1993, _1995,
    _1997, _2000, _2001, _2002,
    _2005, _2007, _2009, _2011,
    _2013
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2017, _2020, _2023
from mastapy.system_model.connections_and_sockets.couplings import (
    _2024, _2026, _2028, _2030,
    _2032, _2034
)
from mastapy.system_model.part_model import (
    _2114, _2115, _2116, _2117,
    _2120, _2122, _2123, _2124,
    _2127, _2128, _2131, _2132,
    _2133, _2134, _2141, _2142,
    _2143, _2145, _2147, _2148,
    _2150, _2151, _2153, _2155,
    _2156, _2157
)
from mastapy.system_model.part_model.shaft_model import _2160
from mastapy.system_model.part_model.gears import (
    _2190, _2191, _2192, _2193,
    _2194, _2195, _2196, _2197,
    _2198, _2199, _2200, _2201,
    _2202, _2203, _2204, _2205,
    _2206, _2207, _2209, _2211,
    _2212, _2213, _2214, _2215,
    _2216, _2217, _2218, _2219,
    _2220, _2221, _2222, _2223,
    _2224, _2225, _2226, _2227,
    _2228, _2229, _2230, _2231
)
from mastapy.system_model.part_model.cycloidal import _2245, _2246, _2247
from mastapy.system_model.part_model.couplings import (
    _2253, _2255, _2256, _2258,
    _2259, _2260, _2261, _2263,
    _2264, _2265, _2266, _2267,
    _2273, _2274, _2275, _2277,
    _2278, _2279, _2281, _2282,
    _2283, _2284, _2285, _2287
)
from mastapy._math.color import Color
from mastapy._math.vector_3d import Vector3D
from mastapy.utility.operation_modes import _1523
from mastapy.math_utility import _1257, _1276
from mastapy.nodal_analysis.space_claim_link import _119
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_FACETED_BODY = python_net_import('SMT.MastaAPI.MathUtility', 'FacetedBody')
_STRING = python_net_import('System', 'String')
_MASTAGUI = python_net_import('SMT.MastaAPI.SystemModelGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_0.APIBase):
    '''MASTAGUI

    This is a mastapy class.
    '''

    TYPE = _MASTAGUI

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_paused(self) -> 'bool':
        '''bool: 'IsPaused' is the original name of this property.'''

        return self.wrapped.IsPaused

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def is_initialised(self) -> 'bool':
        '''bool: 'IsInitialised' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInitialised

    @property
    def is_remoting(self) -> 'bool':
        '''bool: 'IsRemoting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsRemoting

    @property
    def selected_design_entity(self) -> '_1893.DesignEntity':
        '''DesignEntity: 'SelectedDesignEntity' is the original name of this property.'''

        if _1893.DesignEntity.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to DesignEntity. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity.setter
    def selected_design_entity(self, value: '_1893.DesignEntity'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1947.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1947.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self, value: '_1947.AbstractShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_connection(self) -> '_1950.BeltConnection':
        '''BeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1950.BeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_belt_connection.setter
    def selected_design_entity_of_type_belt_connection(self, value: '_1950.BeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coaxial_connection(self) -> '_1951.CoaxialConnection':
        '''CoaxialConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1951.CoaxialConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CoaxialConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coaxial_connection.setter
    def selected_design_entity_of_type_coaxial_connection(self, value: '_1951.CoaxialConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connection(self) -> '_1954.Connection':
        '''Connection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1954.Connection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_connection.setter
    def selected_design_entity_of_type_connection(self, value: '_1954.Connection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_belt_connection(self) -> '_1955.CVTBeltConnection':
        '''CVTBeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1955.CVTBeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTBeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt_belt_connection.setter
    def selected_design_entity_of_type_cvt_belt_connection(self, value: '_1955.CVTBeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_inter_mountable_component_connection(self) -> '_1963.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1963.InterMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_inter_mountable_component_connection.setter
    def selected_design_entity_of_type_inter_mountable_component_connection(self, value: '_1963.InterMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_connection(self) -> '_1969.PlanetaryConnection':
        '''PlanetaryConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1969.PlanetaryConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planetary_connection.setter
    def selected_design_entity_of_type_planetary_connection(self, value: '_1969.PlanetaryConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_connection(self) -> '_1974.RollingRingConnection':
        '''RollingRingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1974.RollingRingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring_connection.setter
    def selected_design_entity_of_type_rolling_ring_connection(self, value: '_1974.RollingRingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self) -> '_1977.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _1977.ShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self, value: '_1977.ShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self) -> '_1981.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1981.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_mesh.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self, value: '_1981.AGMAGleasonConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self) -> '_1983.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1983.BevelDifferentialGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear_mesh.setter
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self, value: '_1983.BevelDifferentialGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_mesh(self) -> '_1985.BevelGearMesh':
        '''BevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1985.BevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear_mesh.setter
    def selected_design_entity_of_type_bevel_gear_mesh(self, value: '_1985.BevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_mesh(self) -> '_1987.ConceptGearMesh':
        '''ConceptGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1987.ConceptGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear_mesh.setter
    def selected_design_entity_of_type_concept_gear_mesh(self, value: '_1987.ConceptGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_mesh(self) -> '_1989.ConicalGearMesh':
        '''ConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1989.ConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear_mesh.setter
    def selected_design_entity_of_type_conical_gear_mesh(self, value: '_1989.ConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_mesh(self) -> '_1991.CylindricalGearMesh':
        '''CylindricalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1991.CylindricalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear_mesh.setter
    def selected_design_entity_of_type_cylindrical_gear_mesh(self, value: '_1991.CylindricalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_mesh(self) -> '_1993.FaceGearMesh':
        '''FaceGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1993.FaceGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear_mesh.setter
    def selected_design_entity_of_type_face_gear_mesh(self, value: '_1993.FaceGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_mesh(self) -> '_1995.GearMesh':
        '''GearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1995.GearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear_mesh.setter
    def selected_design_entity_of_type_gear_mesh(self, value: '_1995.GearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_mesh(self) -> '_1997.HypoidGearMesh':
        '''HypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _1997.HypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_hypoid_gear_mesh(self, value: '_1997.HypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2000.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2000.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self, value: '_2000.KlingelnbergCycloPalloidConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2001.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2001.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, value: '_2001.KlingelnbergCycloPalloidHypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2002.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2002.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, value: '_2002.KlingelnbergCycloPalloidSpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self) -> '_2005.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2005.SpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self, value: '_2005.SpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self) -> '_2007.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2007.StraightBevelDiffGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self, value: '_2007.StraightBevelDiffGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self) -> '_2009.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2009.StraightBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self, value: '_2009.StraightBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_mesh(self) -> '_2011.WormGearMesh':
        '''WormGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2011.WormGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear_mesh.setter
    def selected_design_entity_of_type_worm_gear_mesh(self, value: '_2011.WormGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self) -> '_2013.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2013.ZerolBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear_mesh.setter
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self, value: '_2013.ZerolBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2017.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2017.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc_central_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self, value: '_2017.CycloidalDiscCentralBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2020.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2020.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self, value: '_2020.CycloidalDiscPlanetaryBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self) -> '_2023.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2023.RingPinsToDiscConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_ring_pins_to_disc_connection.setter
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self, value: '_2023.RingPinsToDiscConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_connection(self) -> '_2024.ClutchConnection':
        '''ClutchConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2024.ClutchConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch_connection.setter
    def selected_design_entity_of_type_clutch_connection(self, value: '_2024.ClutchConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_connection(self) -> '_2026.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2026.ConceptCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling_connection.setter
    def selected_design_entity_of_type_concept_coupling_connection(self, value: '_2026.ConceptCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_connection(self) -> '_2028.CouplingConnection':
        '''CouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2028.CouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling_connection.setter
    def selected_design_entity_of_type_coupling_connection(self, value: '_2028.CouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self) -> '_2030.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2030.PartToPartShearCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_connection.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self, value: '_2030.PartToPartShearCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_connection(self) -> '_2032.SpringDamperConnection':
        '''SpringDamperConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2032.SpringDamperConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper_connection.setter
    def selected_design_entity_of_type_spring_damper_connection(self, value: '_2032.SpringDamperConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_connection(self) -> '_2034.TorqueConverterConnection':
        '''TorqueConverterConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2034.TorqueConverterConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_connection.setter
    def selected_design_entity_of_type_torque_converter_connection(self, value: '_2034.TorqueConverterConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_assembly(self) -> '_2114.Assembly':
        '''Assembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2114.Assembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Assembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_assembly.setter
    def selected_design_entity_of_type_assembly(self, value: '_2114.Assembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_assembly(self) -> '_2115.AbstractAssembly':
        '''AbstractAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2115.AbstractAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_assembly.setter
    def selected_design_entity_of_type_abstract_assembly(self, value: '_2115.AbstractAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft(self) -> '_2116.AbstractShaft':
        '''AbstractShaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2116.AbstractShaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft.setter
    def selected_design_entity_of_type_abstract_shaft(self, value: '_2116.AbstractShaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_or_housing(self) -> '_2117.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2117.AbstractShaftOrHousing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_abstract_shaft_or_housing.setter
    def selected_design_entity_of_type_abstract_shaft_or_housing(self, value: '_2117.AbstractShaftOrHousing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bearing(self) -> '_2120.Bearing':
        '''Bearing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2120.Bearing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bearing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bearing.setter
    def selected_design_entity_of_type_bearing(self, value: '_2120.Bearing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolt(self) -> '_2122.Bolt':
        '''Bolt: 'SelectedDesignEntity' is the original name of this property.'''

        if _2122.Bolt.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bolt. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bolt.setter
    def selected_design_entity_of_type_bolt(self, value: '_2122.Bolt'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolted_joint(self) -> '_2123.BoltedJoint':
        '''BoltedJoint: 'SelectedDesignEntity' is the original name of this property.'''

        if _2123.BoltedJoint.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BoltedJoint. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bolted_joint.setter
    def selected_design_entity_of_type_bolted_joint(self, value: '_2123.BoltedJoint'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_component(self) -> '_2124.Component':
        '''Component: 'SelectedDesignEntity' is the original name of this property.'''

        if _2124.Component.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Component. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_component.setter
    def selected_design_entity_of_type_component(self, value: '_2124.Component'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connector(self) -> '_2127.Connector':
        '''Connector: 'SelectedDesignEntity' is the original name of this property.'''

        if _2127.Connector.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connector. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_connector.setter
    def selected_design_entity_of_type_connector(self, value: '_2127.Connector'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_datum(self) -> '_2128.Datum':
        '''Datum: 'SelectedDesignEntity' is the original name of this property.'''

        if _2128.Datum.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Datum. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_datum.setter
    def selected_design_entity_of_type_datum(self, value: '_2128.Datum'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_external_cad_model(self) -> '_2131.ExternalCADModel':
        '''ExternalCADModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2131.ExternalCADModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ExternalCADModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_external_cad_model.setter
    def selected_design_entity_of_type_external_cad_model(self, value: '_2131.ExternalCADModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_fe_part(self) -> '_2132.FEPart':
        '''FEPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2132.FEPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FEPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_fe_part.setter
    def selected_design_entity_of_type_fe_part(self, value: '_2132.FEPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_flexible_pin_assembly(self) -> '_2133.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2133.FlexiblePinAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_flexible_pin_assembly.setter
    def selected_design_entity_of_type_flexible_pin_assembly(self, value: '_2133.FlexiblePinAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_guide_dxf_model(self) -> '_2134.GuideDxfModel':
        '''GuideDxfModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2134.GuideDxfModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GuideDxfModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_guide_dxf_model.setter
    def selected_design_entity_of_type_guide_dxf_model(self, value: '_2134.GuideDxfModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mass_disc(self) -> '_2141.MassDisc':
        '''MassDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2141.MassDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MassDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_mass_disc.setter
    def selected_design_entity_of_type_mass_disc(self, value: '_2141.MassDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_measurement_component(self) -> '_2142.MeasurementComponent':
        '''MeasurementComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2142.MeasurementComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MeasurementComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_measurement_component.setter
    def selected_design_entity_of_type_measurement_component(self, value: '_2142.MeasurementComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mountable_component(self) -> '_2143.MountableComponent':
        '''MountableComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2143.MountableComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MountableComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_mountable_component.setter
    def selected_design_entity_of_type_mountable_component(self, value: '_2143.MountableComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_oil_seal(self) -> '_2145.OilSeal':
        '''OilSeal: 'SelectedDesignEntity' is the original name of this property.'''

        if _2145.OilSeal.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to OilSeal. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_oil_seal.setter
    def selected_design_entity_of_type_oil_seal(self, value: '_2145.OilSeal'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part(self) -> '_2147.Part':
        '''Part: 'SelectedDesignEntity' is the original name of this property.'''

        if _2147.Part.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Part. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part.setter
    def selected_design_entity_of_type_part(self, value: '_2147.Part'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planet_carrier(self) -> '_2148.PlanetCarrier':
        '''PlanetCarrier: 'SelectedDesignEntity' is the original name of this property.'''

        if _2148.PlanetCarrier.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetCarrier. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planet_carrier.setter
    def selected_design_entity_of_type_planet_carrier(self, value: '_2148.PlanetCarrier'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_point_load(self) -> '_2150.PointLoad':
        '''PointLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2150.PointLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PointLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_point_load.setter
    def selected_design_entity_of_type_point_load(self, value: '_2150.PointLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_power_load(self) -> '_2151.PowerLoad':
        '''PowerLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2151.PowerLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PowerLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_power_load.setter
    def selected_design_entity_of_type_power_load(self, value: '_2151.PowerLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_root_assembly(self) -> '_2153.RootAssembly':
        '''RootAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2153.RootAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RootAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_root_assembly.setter
    def selected_design_entity_of_type_root_assembly(self, value: '_2153.RootAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_specialised_assembly(self) -> '_2155.SpecialisedAssembly':
        '''SpecialisedAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2155.SpecialisedAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_specialised_assembly.setter
    def selected_design_entity_of_type_specialised_assembly(self, value: '_2155.SpecialisedAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_unbalanced_mass(self) -> '_2156.UnbalancedMass':
        '''UnbalancedMass: 'SelectedDesignEntity' is the original name of this property.'''

        if _2156.UnbalancedMass.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to UnbalancedMass. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_unbalanced_mass.setter
    def selected_design_entity_of_type_unbalanced_mass(self, value: '_2156.UnbalancedMass'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_virtual_component(self) -> '_2157.VirtualComponent':
        '''VirtualComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2157.VirtualComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to VirtualComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_virtual_component.setter
    def selected_design_entity_of_type_virtual_component(self, value: '_2157.VirtualComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft(self) -> '_2160.Shaft':
        '''Shaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2160.Shaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Shaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft.setter
    def selected_design_entity_of_type_shaft(self, value: '_2160.Shaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear(self) -> '_2190.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2190.AGMAGleasonConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear(self, value: '_2190.AGMAGleasonConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self) -> '_2191.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2191.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_set.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self, value: '_2191.AGMAGleasonConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear(self) -> '_2192.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2192.BevelDifferentialGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear.setter
    def selected_design_entity_of_type_bevel_differential_gear(self, value: '_2192.BevelDifferentialGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_set(self) -> '_2193.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2193.BevelDifferentialGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_gear_set.setter
    def selected_design_entity_of_type_bevel_differential_gear_set(self, value: '_2193.BevelDifferentialGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_planet_gear(self) -> '_2194.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2194.BevelDifferentialPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_planet_gear.setter
    def selected_design_entity_of_type_bevel_differential_planet_gear(self, value: '_2194.BevelDifferentialPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_sun_gear(self) -> '_2195.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2195.BevelDifferentialSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_differential_sun_gear.setter
    def selected_design_entity_of_type_bevel_differential_sun_gear(self, value: '_2195.BevelDifferentialSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear(self) -> '_2196.BevelGear':
        '''BevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2196.BevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear.setter
    def selected_design_entity_of_type_bevel_gear(self, value: '_2196.BevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_set(self) -> '_2197.BevelGearSet':
        '''BevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2197.BevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_bevel_gear_set.setter
    def selected_design_entity_of_type_bevel_gear_set(self, value: '_2197.BevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear(self) -> '_2198.ConceptGear':
        '''ConceptGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2198.ConceptGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear.setter
    def selected_design_entity_of_type_concept_gear(self, value: '_2198.ConceptGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_set(self) -> '_2199.ConceptGearSet':
        '''ConceptGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2199.ConceptGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_gear_set.setter
    def selected_design_entity_of_type_concept_gear_set(self, value: '_2199.ConceptGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear(self) -> '_2200.ConicalGear':
        '''ConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2200.ConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear.setter
    def selected_design_entity_of_type_conical_gear(self, value: '_2200.ConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_set(self) -> '_2201.ConicalGearSet':
        '''ConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2201.ConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_conical_gear_set.setter
    def selected_design_entity_of_type_conical_gear_set(self, value: '_2201.ConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear(self) -> '_2202.CylindricalGear':
        '''CylindricalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2202.CylindricalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear.setter
    def selected_design_entity_of_type_cylindrical_gear(self, value: '_2202.CylindricalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_set(self) -> '_2203.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2203.CylindricalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_gear_set.setter
    def selected_design_entity_of_type_cylindrical_gear_set(self, value: '_2203.CylindricalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_planet_gear(self) -> '_2204.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2204.CylindricalPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cylindrical_planet_gear.setter
    def selected_design_entity_of_type_cylindrical_planet_gear(self, value: '_2204.CylindricalPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear(self) -> '_2205.FaceGear':
        '''FaceGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2205.FaceGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear.setter
    def selected_design_entity_of_type_face_gear(self, value: '_2205.FaceGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_set(self) -> '_2206.FaceGearSet':
        '''FaceGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2206.FaceGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_face_gear_set.setter
    def selected_design_entity_of_type_face_gear_set(self, value: '_2206.FaceGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear(self) -> '_2207.Gear':
        '''Gear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2207.Gear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Gear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear.setter
    def selected_design_entity_of_type_gear(self, value: '_2207.Gear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_set(self) -> '_2209.GearSet':
        '''GearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2209.GearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_gear_set.setter
    def selected_design_entity_of_type_gear_set(self, value: '_2209.GearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear(self) -> '_2211.HypoidGear':
        '''HypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2211.HypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear.setter
    def selected_design_entity_of_type_hypoid_gear(self, value: '_2211.HypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_set(self) -> '_2212.HypoidGearSet':
        '''HypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2212.HypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_hypoid_gear_set.setter
    def selected_design_entity_of_type_hypoid_gear_set(self, value: '_2212.HypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2213.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2213.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self, value: '_2213.KlingelnbergCycloPalloidConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2214.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2214.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, value: '_2214.KlingelnbergCycloPalloidConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2215.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2215.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, value: '_2215.KlingelnbergCycloPalloidHypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2216.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2216.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, value: '_2216.KlingelnbergCycloPalloidHypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2217.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2217.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, value: '_2217.KlingelnbergCycloPalloidSpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2218.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2218.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, value: '_2218.KlingelnbergCycloPalloidSpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_gear_set(self) -> '_2219.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2219.PlanetaryGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_planetary_gear_set.setter
    def selected_design_entity_of_type_planetary_gear_set(self, value: '_2219.PlanetaryGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear(self) -> '_2220.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2220.SpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear.setter
    def selected_design_entity_of_type_spiral_bevel_gear(self, value: '_2220.SpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_set(self) -> '_2221.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2221.SpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_spiral_bevel_gear_set(self, value: '_2221.SpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear(self) -> '_2222.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2222.StraightBevelDiffGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear(self, value: '_2222.StraightBevelDiffGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self) -> '_2223.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2223.StraightBevelDiffGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self, value: '_2223.StraightBevelDiffGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear(self) -> '_2224.StraightBevelGear':
        '''StraightBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2224.StraightBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear.setter
    def selected_design_entity_of_type_straight_bevel_gear(self, value: '_2224.StraightBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_set(self) -> '_2225.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2225.StraightBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_gear_set(self, value: '_2225.StraightBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_planet_gear(self) -> '_2226.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2226.StraightBevelPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_planet_gear.setter
    def selected_design_entity_of_type_straight_bevel_planet_gear(self, value: '_2226.StraightBevelPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_sun_gear(self) -> '_2227.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2227.StraightBevelSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_straight_bevel_sun_gear.setter
    def selected_design_entity_of_type_straight_bevel_sun_gear(self, value: '_2227.StraightBevelSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear(self) -> '_2228.WormGear':
        '''WormGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2228.WormGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear.setter
    def selected_design_entity_of_type_worm_gear(self, value: '_2228.WormGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_set(self) -> '_2229.WormGearSet':
        '''WormGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2229.WormGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_worm_gear_set.setter
    def selected_design_entity_of_type_worm_gear_set(self, value: '_2229.WormGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear(self) -> '_2230.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2230.ZerolBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear.setter
    def selected_design_entity_of_type_zerol_bevel_gear(self, value: '_2230.ZerolBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_set(self) -> '_2231.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2231.ZerolBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_zerol_bevel_gear_set.setter
    def selected_design_entity_of_type_zerol_bevel_gear_set(self, value: '_2231.ZerolBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_assembly(self) -> '_2245.CycloidalAssembly':
        '''CycloidalAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2245.CycloidalAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_assembly.setter
    def selected_design_entity_of_type_cycloidal_assembly(self, value: '_2245.CycloidalAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc(self) -> '_2246.CycloidalDisc':
        '''CycloidalDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2246.CycloidalDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cycloidal_disc.setter
    def selected_design_entity_of_type_cycloidal_disc(self, value: '_2246.CycloidalDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins(self) -> '_2247.RingPins':
        '''RingPins: 'SelectedDesignEntity' is the original name of this property.'''

        if _2247.RingPins.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPins. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_ring_pins.setter
    def selected_design_entity_of_type_ring_pins(self, value: '_2247.RingPins'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_drive(self) -> '_2253.BeltDrive':
        '''BeltDrive: 'SelectedDesignEntity' is the original name of this property.'''

        if _2253.BeltDrive.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltDrive. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_belt_drive.setter
    def selected_design_entity_of_type_belt_drive(self, value: '_2253.BeltDrive'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch(self) -> '_2255.Clutch':
        '''Clutch: 'SelectedDesignEntity' is the original name of this property.'''

        if _2255.Clutch.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Clutch. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch.setter
    def selected_design_entity_of_type_clutch(self, value: '_2255.Clutch'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_half(self) -> '_2256.ClutchHalf':
        '''ClutchHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2256.ClutchHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_clutch_half.setter
    def selected_design_entity_of_type_clutch_half(self, value: '_2256.ClutchHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling(self) -> '_2258.ConceptCoupling':
        '''ConceptCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2258.ConceptCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling.setter
    def selected_design_entity_of_type_concept_coupling(self, value: '_2258.ConceptCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_half(self) -> '_2259.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2259.ConceptCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_concept_coupling_half.setter
    def selected_design_entity_of_type_concept_coupling_half(self, value: '_2259.ConceptCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling(self) -> '_2260.Coupling':
        '''Coupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2260.Coupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Coupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling.setter
    def selected_design_entity_of_type_coupling(self, value: '_2260.Coupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_half(self) -> '_2261.CouplingHalf':
        '''CouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2261.CouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_coupling_half.setter
    def selected_design_entity_of_type_coupling_half(self, value: '_2261.CouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt(self) -> '_2263.CVT':
        '''CVT: 'SelectedDesignEntity' is the original name of this property.'''

        if _2263.CVT.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVT. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt.setter
    def selected_design_entity_of_type_cvt(self, value: '_2263.CVT'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_pulley(self) -> '_2264.CVTPulley':
        '''CVTPulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2264.CVTPulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTPulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_cvt_pulley.setter
    def selected_design_entity_of_type_cvt_pulley(self, value: '_2264.CVTPulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling(self) -> '_2265.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2265.PartToPartShearCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling(self, value: '_2265.PartToPartShearCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self) -> '_2266.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2266.PartToPartShearCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_half.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self, value: '_2266.PartToPartShearCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_pulley(self) -> '_2267.Pulley':
        '''Pulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2267.Pulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Pulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_pulley.setter
    def selected_design_entity_of_type_pulley(self, value: '_2267.Pulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring(self) -> '_2273.RollingRing':
        '''RollingRing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2273.RollingRing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring.setter
    def selected_design_entity_of_type_rolling_ring(self, value: '_2273.RollingRing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_assembly(self) -> '_2274.RollingRingAssembly':
        '''RollingRingAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2274.RollingRingAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_rolling_ring_assembly.setter
    def selected_design_entity_of_type_rolling_ring_assembly(self, value: '_2274.RollingRingAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_hub_connection(self) -> '_2275.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2275.ShaftHubConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftHubConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_shaft_hub_connection.setter
    def selected_design_entity_of_type_shaft_hub_connection(self, value: '_2275.ShaftHubConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper(self) -> '_2277.SpringDamper':
        '''SpringDamper: 'SelectedDesignEntity' is the original name of this property.'''

        if _2277.SpringDamper.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamper. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper.setter
    def selected_design_entity_of_type_spring_damper(self, value: '_2277.SpringDamper'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_half(self) -> '_2278.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2278.SpringDamperHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_spring_damper_half.setter
    def selected_design_entity_of_type_spring_damper_half(self, value: '_2278.SpringDamperHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser(self) -> '_2279.Synchroniser':
        '''Synchroniser: 'SelectedDesignEntity' is the original name of this property.'''

        if _2279.Synchroniser.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Synchroniser. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser.setter
    def selected_design_entity_of_type_synchroniser(self, value: '_2279.Synchroniser'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_half(self) -> '_2281.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2281.SynchroniserHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_half.setter
    def selected_design_entity_of_type_synchroniser_half(self, value: '_2281.SynchroniserHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_part(self) -> '_2282.SynchroniserPart':
        '''SynchroniserPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2282.SynchroniserPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_part.setter
    def selected_design_entity_of_type_synchroniser_part(self, value: '_2282.SynchroniserPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_sleeve(self) -> '_2283.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedDesignEntity' is the original name of this property.'''

        if _2283.SynchroniserSleeve.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_synchroniser_sleeve.setter
    def selected_design_entity_of_type_synchroniser_sleeve(self, value: '_2283.SynchroniserSleeve'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter(self) -> '_2284.TorqueConverter':
        '''TorqueConverter: 'SelectedDesignEntity' is the original name of this property.'''

        if _2284.TorqueConverter.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverter. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter.setter
    def selected_design_entity_of_type_torque_converter(self, value: '_2284.TorqueConverter'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_pump(self) -> '_2285.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedDesignEntity' is the original name of this property.'''

        if _2285.TorqueConverterPump.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterPump. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_pump.setter
    def selected_design_entity_of_type_torque_converter_pump(self, value: '_2285.TorqueConverterPump'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_turbine(self) -> '_2287.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedDesignEntity' is the original name of this property.'''

        if _2287.TorqueConverterTurbine.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity else None

    @selected_design_entity_of_type_torque_converter_turbine.setter
    def selected_design_entity_of_type_torque_converter_turbine(self, value: '_2287.TorqueConverterTurbine'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def active_design(self) -> '_1889.Design':
        '''Design: 'ActiveDesign' is the original name of this property.'''

        return constructor.new(_1889.Design)(self.wrapped.ActiveDesign) if self.wrapped.ActiveDesign else None

    @active_design.setter
    def active_design(self, value: '_1889.Design'):
        value = value.wrapped if value else None
        self.wrapped.ActiveDesign = value

    @property
    def restart_space_claim_flag(self) -> 'bool':
        '''bool: 'RestartSpaceClaimFlag' is the original name of this property.'''

        return self.wrapped.RestartSpaceClaimFlag

    @restart_space_claim_flag.setter
    def restart_space_claim_flag(self, value: 'bool'):
        self.wrapped.RestartSpaceClaimFlag = bool(value) if value else False

    @property
    def space_claim_process_id(self) -> 'int':
        '''int: 'SpaceClaimProcessID' is the original name of this property.'''

        return self.wrapped.SpaceClaimProcessID

    @space_claim_process_id.setter
    def space_claim_process_id(self, value: 'int'):
        self.wrapped.SpaceClaimProcessID = int(value) if value else 0

    @property
    def restart_space_claim_save_file(self) -> 'str':
        '''str: 'RestartSpaceClaimSaveFile' is the original name of this property.'''

        return self.wrapped.RestartSpaceClaimSaveFile

    @restart_space_claim_save_file.setter
    def restart_space_claim_save_file(self, value: 'str'):
        self.wrapped.RestartSpaceClaimSaveFile = str(value) if value else None

    @property
    def color_of_new_problem_node_group(self) -> 'Color':
        '''Color: 'ColorOfNewProblemNodeGroup' is the original name of this property.'''

        value = conversion.pn_to_mp_color(self.wrapped.ColorOfNewProblemNodeGroup)
        return value

    @color_of_new_problem_node_group.setter
    def color_of_new_problem_node_group(self, value: 'Color'):
        value = value if value else None
        value = conversion.mp_to_pn_color(value)
        self.wrapped.ColorOfNewProblemNodeGroup = value

    @property
    def name_of_new_problem_node_group(self) -> 'str':
        '''str: 'NameOfNewProblemNodeGroup' is the original name of this property.'''

        return self.wrapped.NameOfNewProblemNodeGroup

    @name_of_new_problem_node_group.setter
    def name_of_new_problem_node_group(self, value: 'str'):
        self.wrapped.NameOfNewProblemNodeGroup = str(value) if value else None

    @property
    def positions_of_problem_node_group(self) -> 'List[Vector3D]':
        '''List[Vector3D]: 'PositionsOfProblemNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PositionsOfProblemNodeGroup, Vector3D)
        return value

    @property
    def operation_mode(self) -> '_1523.OperationMode':
        '''OperationMode: 'OperationMode' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OperationMode)
        return constructor.new(_1523.OperationMode)(value) if value else None

    @operation_mode.setter
    def operation_mode(self, value: '_1523.OperationMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OperationMode = value

    @property
    def is_connected_to_space_claim(self) -> 'bool':
        '''bool: 'IsConnectedToSpaceClaim' is the original name of this property.'''

        return self.wrapped.IsConnectedToSpaceClaim

    @is_connected_to_space_claim.setter
    def is_connected_to_space_claim(self, value: 'bool'):
        self.wrapped.IsConnectedToSpaceClaim = bool(value) if value else False

    @property
    def process_id(self) -> 'int':
        '''int: 'ProcessId' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProcessId

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    @staticmethod
    def get_mastagui(process_id: 'int') -> 'MASTAGUI':
        ''' 'GetMASTAGUI' is the original name of this method.

        Args:
            process_id (int)

        Returns:
            mastapy.system_model_gui.MASTAGUI
        '''

        process_id = int(process_id)
        method_result = MASTAGUI.TYPE.GetMASTAGUI(process_id if process_id else 0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def resume(self):
        ''' 'Resume' is the original name of this method.'''

        self.wrapped.Resume()

    def pause(self):
        ''' 'Pause' is the original name of this method.'''

        self.wrapped.Pause()

    def start_remoting(self):
        ''' 'StartRemoting' is the original name of this method.'''

        self.wrapped.StartRemoting()

    def stop_remoting(self):
        ''' 'StopRemoting' is the original name of this method.'''

        self.wrapped.StopRemoting()

    def open_design_in_new_tab(self, design: '_1889.Design'):
        ''' 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        '''

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def select_tab(self, tab_text: 'str'):
        ''' 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        '''

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else None)

    def move_selected_component(self, origin: 'Vector3D', axis: 'Vector3D'):
        ''' 'MoveSelectedComponent' is the original name of this method.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        '''

        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        self.wrapped.MoveSelectedComponent(origin, axis)

    def run_command(self, command: 'str'):
        ''' 'RunCommand' is the original name of this method.

        Args:
            command (str)
        '''

        command = str(command)
        self.wrapped.RunCommand(command if command else None)

    def add_line_from_space_claim(self, circles_on_axis: '_1257.CirclesOnAxis'):
        ''' 'AddLineFromSpaceClaim' is the original name of this method.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        '''

        self.wrapped.AddLineFromSpaceClaim(circles_on_axis.wrapped if circles_on_axis else None)

    def show_boxes(self, small_box: 'List[Vector3D]', big_box: 'List[Vector3D]'):
        ''' 'ShowBoxes' is the original name of this method.

        Args:
            small_box (List[Vector3D])
            big_box (List[Vector3D])
        '''

        small_box = conversion.mp_to_pn_objects_in_list(small_box)
        big_box = conversion.mp_to_pn_objects_in_list(big_box)
        self.wrapped.ShowBoxes(small_box, big_box)

    def circle_pairs_from_space_claim(self, preselection_circles: '_1257.CirclesOnAxis', selected_circles: 'List[_1257.CirclesOnAxis]'):
        ''' 'CirclePairsFromSpaceClaim' is the original name of this method.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        '''

        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        self.wrapped.CirclePairsFromSpaceClaim(preselection_circles.wrapped if preselection_circles else None, selected_circles)

    def add_fe_substructure_from_data(self, vertices_and_facets: '_1276.FacetedBody', dimensions: 'Dict[str, _119.SpaceClaimDimension]', moniker: 'str'):
        ''' 'AddFESubstructureFromData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
            moniker (str)
        '''

        moniker = str(moniker)
        self.wrapped.AddFESubstructureFromData(vertices_and_facets.wrapped if vertices_and_facets else None, dimensions, moniker if moniker else None)

    def add_fe_substructure_from_file(self, length_scale: 'float', stl_file_name: 'str', dimensions: 'Dict[str, _119.SpaceClaimDimension]'):
        ''' 'AddFESubstructureFromFile' is the original name of this method.

        Args:
            length_scale (float)
            stl_file_name (str)
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
        '''

        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        self.wrapped.AddFESubstructureFromFile(length_scale if length_scale else 0.0, stl_file_name if stl_file_name else None, dimensions)

    def flag_message_received(self):
        ''' 'FlagMessageReceived' is the original name of this method.'''

        self.wrapped.FlagMessageReceived()

    def space_claim_document_loaded(self):
        ''' 'SpaceClaimDocumentLoaded' is the original name of this method.'''

        self.wrapped.SpaceClaimDocumentLoaded()

    def set_error(self, error: 'str'):
        ''' 'SetError' is the original name of this method.

        Args:
            error (str)
        '''

        error = str(error)
        self.wrapped.SetError(error if error else None)

    def new_dimensions(self, dimensions: 'Dict[str, _119.SpaceClaimDimension]'):
        ''' 'NewDimensions' is the original name of this method.

        Args:
            dimensions (Dict[str, mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension])
        '''

        self.wrapped.NewDimensions(dimensions)

    def create_space_claim_dimension(self) -> '_119.SpaceClaimDimension':
        ''' 'CreateSpaceClaimDimension' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.space_claim_link.SpaceClaimDimension
        '''

        method_result = self.wrapped.CreateSpaceClaimDimension()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def new_mesh_data(self, vertices_and_facets: '_1276.FacetedBody'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
        '''

        self.wrapped.NewMeshData.Overloads[_FACETED_BODY](vertices_and_facets.wrapped if vertices_and_facets else None)

    def new_mesh_data_from_file(self, stl_file_name: 'str'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            stl_file_name (str)
        '''

        stl_file_name = str(stl_file_name)
        self.wrapped.NewMeshData.Overloads[_STRING](stl_file_name if stl_file_name else None)

    def create_new_circles_on_axis(self) -> '_1257.CirclesOnAxis':
        ''' 'CreateNewCirclesOnAxis' is the original name of this method.

        Returns:
            mastapy.math_utility.CirclesOnAxis
        '''

        method_result = self.wrapped.CreateNewCirclesOnAxis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def create_new_faceted_body(self) -> '_1276.FacetedBody':
        ''' 'CreateNewFacetedBody' is the original name of this method.

        Returns:
            mastapy.math_utility.FacetedBody
        '''

        method_result = self.wrapped.CreateNewFacetedBody()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
