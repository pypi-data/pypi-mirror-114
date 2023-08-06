'''_292.py

GearSetOptimisationResult
'''


from mastapy.gears.gear_designs import _881
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _885
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _890
from mastapy.gears.gear_designs.straight_bevel_diff import _894
from mastapy.gears.gear_designs.straight_bevel import _898
from mastapy.gears.gear_designs.spiral_bevel import _902
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _906
from mastapy.gears.gear_designs.klingelnberg_hypoid import _910
from mastapy.gears.gear_designs.klingelnberg_conical import _914
from mastapy.gears.gear_designs.hypoid import _918
from mastapy.gears.gear_designs.face import _926
from mastapy.gears.gear_designs.cylindrical import _957, _968
from mastapy.gears.gear_designs.conical import _1069
from mastapy.gears.gear_designs.concept import _1091
from mastapy.gears.gear_designs.bevel import _1095
from mastapy.gears.gear_designs.agma_gleason_conical import _1108
from mastapy.gears.rating import _317, _324, _325
from mastapy.gears.rating.zerol_bevel import _333
from mastapy.gears.rating.worm import _337, _338
from mastapy.gears.rating.straight_bevel_diff import _359
from mastapy.gears.rating.straight_bevel import _363
from mastapy.gears.rating.spiral_bevel import _366
from mastapy.gears.rating.klingelnberg_spiral_bevel import _369
from mastapy.gears.rating.klingelnberg_hypoid import _372
from mastapy.gears.rating.klingelnberg_conical import _375
from mastapy.gears.rating.hypoid import _402
from mastapy.gears.rating.face import _411, _412
from mastapy.gears.rating.cylindrical import _423, _424
from mastapy.gears.rating.conical import _490, _491
from mastapy.gears.rating.concept import _501, _502
from mastapy.gears.rating.bevel import _505
from mastapy.gears.rating.agma_gleason_conical import _516
from mastapy.math_utility.optimisation import _1307
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISATION_RESULT = python_net_import('SMT.MastaAPI.Gears', 'GearSetOptimisationResult')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimisationResult',)


class GearSetOptimisationResult(_0.APIBase):
    '''GearSetOptimisationResult

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISATION_RESULT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimisationResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set(self) -> '_881.GearSetDesign':
        '''GearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _881.GearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to GearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_zerol_bevel_gear_set_design(self) -> '_885.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _885.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_worm_gear_set_design(self) -> '_890.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _890.WormGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_diff_gear_set_design(self) -> '_894.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _894.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_gear_set_design(self) -> '_898.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _898.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_spiral_bevel_gear_set_design(self) -> '_902.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _902.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_906.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _906.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_910.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _910.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_conical_gear_set_design(self) -> '_914.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _914.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_hypoid_gear_set_design(self) -> '_918.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _918.HypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_face_gear_set_design(self) -> '_926.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _926.FaceGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_gear_set_design(self) -> '_957.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _957.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_cylindrical_planetary_gear_set_design(self) -> '_968.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _968.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_conical_gear_set_design(self) -> '_1069.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1069.ConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_concept_gear_set_design(self) -> '_1091.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1091.ConceptGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_bevel_gear_set_design(self) -> '_1095.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1095.BevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_agma_gleason_conical_gear_set_design(self) -> '_1108.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1108.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSet.__class__)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def rating(self) -> '_317.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _317.AbstractGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AbstractGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_duty_cycle_rating(self) -> '_324.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _324.GearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_gear_set_rating(self) -> '_325.GearSetRating':
        '''GearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.GearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to GearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_zerol_bevel_gear_set_rating(self) -> '_333.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _333.ZerolBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_337.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_worm_gear_set_rating(self) -> '_338.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _338.WormGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to WormGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_diff_gear_set_rating(self) -> '_359.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _359.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_straight_bevel_gear_set_rating(self) -> '_363.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _363.StraightBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_spiral_bevel_gear_set_rating(self) -> '_366.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _366.SpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_369.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _369.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_372.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _372.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_375.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _375.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_hypoid_gear_set_rating(self) -> '_402.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _402.HypoidGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_411.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _411.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_face_gear_set_rating(self) -> '_412.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _412.FaceGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_423.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _423.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_cylindrical_gear_set_rating(self) -> '_424.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _424.CylindricalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_490.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _490.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_conical_gear_set_rating(self) -> '_491.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _491.ConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_501.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_concept_gear_set_rating(self) -> '_502.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.ConceptGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_bevel_gear_set_rating(self) -> '_505.BevelGearSetRating':
        '''BevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _505.BevelGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def rating_of_type_agma_gleason_conical_gear_set_rating(self) -> '_516.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _516.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Rating.__class__.__mro__:
            raise CastException('Failed to cast rating to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Rating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Rating.__class__)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def optimisation_history(self) -> '_1307.OptimisationHistory':
        '''OptimisationHistory: 'OptimisationHistory' is the original name of this property.'''

        return constructor.new(_1307.OptimisationHistory)(self.wrapped.OptimisationHistory) if self.wrapped.OptimisationHistory else None

    @optimisation_history.setter
    def optimisation_history(self, value: '_1307.OptimisationHistory'):
        value = value.wrapped if value else None
        self.wrapped.OptimisationHistory = value

    @property
    def is_optimized(self) -> 'bool':
        '''bool: 'IsOptimized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsOptimized
