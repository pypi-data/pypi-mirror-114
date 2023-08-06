'''_122.py

SpaceClaimSettings
'''


from mastapy._internal import constructor
from mastapy.utility import _1351
from mastapy._internal.python_net import python_net_import

_SPACE_CLAIM_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis.SpaceClaimLink', 'SpaceClaimSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('SpaceClaimSettings',)


class SpaceClaimSettings(_1351.PerMachineSettings):
    '''SpaceClaimSettings

    This is a mastapy class.
    '''

    TYPE = _SPACE_CLAIM_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpaceClaimSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def space_claim_arguments(self) -> 'str':
        '''str: 'SpaceClaimArguments' is the original name of this property.'''

        return self.wrapped.SpaceClaimArguments

    @space_claim_arguments.setter
    def space_claim_arguments(self, value: 'str'):
        self.wrapped.SpaceClaimArguments = str(value) if value else None

    @property
    def folder_path(self) -> 'str':
        '''str: 'FolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderPath

    def edit_folder_path(self):
        ''' 'EditFolderPath' is the original name of this method.'''

        self.wrapped.EditFolderPath()
