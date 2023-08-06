'''_2287.py

ActiveFESubstructureSelection
'''


from mastapy.system_model.part_model.configurations import _2294
from mastapy.system_model.part_model import _2131
from mastapy.system_model.fe import _2063
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelection',)


class ActiveFESubstructureSelection(_2294.PartDetailSelection['_2131.FEPart', '_2063.FESubstructure']):
    '''ActiveFESubstructureSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
