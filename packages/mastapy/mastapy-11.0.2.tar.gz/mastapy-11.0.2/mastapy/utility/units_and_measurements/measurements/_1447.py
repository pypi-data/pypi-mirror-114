'''_1447.py

QuadraticDrag
'''


from mastapy.utility.units_and_measurements import _1362
from mastapy._internal.python_net import python_net_import

_QUADRATIC_DRAG = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'QuadraticDrag')


__docformat__ = 'restructuredtext en'
__all__ = ('QuadraticDrag',)


class QuadraticDrag(_1362.MeasurementBase):
    '''QuadraticDrag

    This is a mastapy class.
    '''

    TYPE = _QUADRATIC_DRAG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'QuadraticDrag.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
