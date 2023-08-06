'''_2244.py

CycloidalAssembly
'''


from mastapy.cycloidal import _1218
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2154
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssembly',)


class CycloidalAssembly(_2154.SpecialisedAssembly):
    '''CycloidalAssembly

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cycloidal_assembly_design(self) -> '_1218.CycloidalAssemblyDesign':
        '''CycloidalAssemblyDesign: 'CycloidalAssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1218.CycloidalAssemblyDesign)(self.wrapped.CycloidalAssemblyDesign) if self.wrapped.CycloidalAssemblyDesign else None
