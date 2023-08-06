'''_5172.py

UnbalancedMassMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2156
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6627
from mastapy.system_model.analyses_and_results.mbd_analyses import _5173
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'UnbalancedMassMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassMultibodyDynamicsAnalysis',)


class UnbalancedMassMultibodyDynamicsAnalysis(_5173.VirtualComponentMultibodyDynamicsAnalysis):
    '''UnbalancedMassMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2156.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6627.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6627.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[UnbalancedMassMultibodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(UnbalancedMassMultibodyDynamicsAnalysis))
        return value
