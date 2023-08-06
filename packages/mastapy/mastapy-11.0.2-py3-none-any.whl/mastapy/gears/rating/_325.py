'''_325.py

GearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.materials import _234
from mastapy.gears.rating import _323, _317
from mastapy._internal.python_net import python_net_import

_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetRating',)


class GearSetRating(_317.AbstractGearSetRating):
    '''GearSetRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def rating(self) -> 'str':
        '''str: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Rating

    @property
    def total_gear_set_reliability(self) -> 'float':
        '''float: 'TotalGearSetReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalGearSetReliability

    @property
    def lubrication_detail(self) -> '_234.LubricationDetail':
        '''LubricationDetail: 'LubricationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_234.LubricationDetail)(self.wrapped.LubricationDetail) if self.wrapped.LubricationDetail else None

    @property
    def gear_ratings(self) -> 'List[_323.GearRating]':
        '''List[GearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_323.GearRating))
        return value
