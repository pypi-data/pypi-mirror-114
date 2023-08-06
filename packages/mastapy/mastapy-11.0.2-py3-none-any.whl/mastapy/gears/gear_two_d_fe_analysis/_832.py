'''_832.py

CylindricalGearSetTIFFAnalysis
'''


from typing import List

from mastapy.gears.gear_two_d_fe_analysis import _833
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _1136
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearSetTIFFAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetTIFFAnalysis',)


class CylindricalGearSetTIFFAnalysis(_1136.GearSetDesignAnalysis):
    '''CylindricalGearSetTIFFAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetTIFFAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gears(self) -> 'List[_833.CylindricalGearTIFFAnalysis]':
        '''List[CylindricalGearTIFFAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_833.CylindricalGearTIFFAnalysis))
        return value
