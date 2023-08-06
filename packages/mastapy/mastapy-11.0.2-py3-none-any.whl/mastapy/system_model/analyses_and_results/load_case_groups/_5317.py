'''_5317.py

AbstractLoadCaseGroup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1889
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4053
from mastapy.system_model.analyses_and_results.static_loads import _6592, _6447, _6459
from mastapy.system_model.analyses_and_results import (
    _2356, _2351, _2334, _2343,
    _2350, _2353, _2354, _2355,
    _2346, _2338, _2337, _2352,
    _2347, _2348, _2357, _2345,
    _2335, _2340, _2341, _2339,
    _2342, _2349, _2336, _2344,
    _2296
)
from mastapy import _7202, _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractLoadCaseGroup',)


class AbstractLoadCaseGroup(_0.APIBase):
    '''AbstractLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractLoadCaseGroup.TYPE'):
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
    def total_duration(self) -> 'float':
        '''float: 'TotalDuration' is the original name of this property.'''

        return self.wrapped.TotalDuration

    @total_duration.setter
    def total_duration(self, value: 'float'):
        self.wrapped.TotalDuration = float(value) if value else 0.0

    @property
    def model(self) -> '_1889.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1889.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def parametric_analysis_options(self) -> '_4053.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4053.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def load_case_root_assemblies(self) -> 'List[_6592.RootAssemblyLoadCase]':
        '''List[RootAssemblyLoadCase]: 'LoadCaseRootAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseRootAssemblies, constructor.new(_6592.RootAssemblyLoadCase))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    @property
    def compound_system_deflection(self) -> '_2356.CompoundSystemDeflectionAnalysis':
        '''CompoundSystemDeflectionAnalysis: 'CompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2356.CompoundSystemDeflectionAnalysis)(self.wrapped.CompoundSystemDeflection) if self.wrapped.CompoundSystemDeflection else None

    @property
    def compound_power_flow(self) -> '_2351.CompoundPowerFlowAnalysis':
        '''CompoundPowerFlowAnalysis: 'CompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2351.CompoundPowerFlowAnalysis)(self.wrapped.CompoundPowerFlow) if self.wrapped.CompoundPowerFlow else None

    @property
    def compound_advanced_system_deflection(self) -> '_2334.CompoundAdvancedSystemDeflectionAnalysis':
        '''CompoundAdvancedSystemDeflectionAnalysis: 'CompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2334.CompoundAdvancedSystemDeflectionAnalysis)(self.wrapped.CompoundAdvancedSystemDeflection) if self.wrapped.CompoundAdvancedSystemDeflection else None

    @property
    def compound_harmonic_analysis(self) -> '_2343.CompoundHarmonicAnalysis':
        '''CompoundHarmonicAnalysis: 'CompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2343.CompoundHarmonicAnalysis)(self.wrapped.CompoundHarmonicAnalysis) if self.wrapped.CompoundHarmonicAnalysis else None

    @property
    def compound_multibody_dynamics_analysis(self) -> '_2350.CompoundMultibodyDynamicsAnalysis':
        '''CompoundMultibodyDynamicsAnalysis: 'CompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2350.CompoundMultibodyDynamicsAnalysis)(self.wrapped.CompoundMultibodyDynamicsAnalysis) if self.wrapped.CompoundMultibodyDynamicsAnalysis else None

    @property
    def compound_steady_state_synchronous_response(self) -> '_2353.CompoundSteadyStateSynchronousResponseAnalysis':
        '''CompoundSteadyStateSynchronousResponseAnalysis: 'CompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2353.CompoundSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponse) if self.wrapped.CompoundSteadyStateSynchronousResponse else None

    @property
    def compound_steady_state_synchronous_response_at_a_speed(self) -> '_2354.CompoundSteadyStateSynchronousResponseAtASpeedAnalysis':
        '''CompoundSteadyStateSynchronousResponseAtASpeedAnalysis: 'CompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2354.CompoundSteadyStateSynchronousResponseAtASpeedAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseAtASpeed) if self.wrapped.CompoundSteadyStateSynchronousResponseAtASpeed else None

    @property
    def compound_steady_state_synchronous_response_on_a_shaft(self) -> '_2355.CompoundSteadyStateSynchronousResponseOnAShaftAnalysis':
        '''CompoundSteadyStateSynchronousResponseOnAShaftAnalysis: 'CompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2355.CompoundSteadyStateSynchronousResponseOnAShaftAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseOnAShaft) if self.wrapped.CompoundSteadyStateSynchronousResponseOnAShaft else None

    @property
    def compound_modal_analysis(self) -> '_2346.CompoundModalAnalysis':
        '''CompoundModalAnalysis: 'CompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2346.CompoundModalAnalysis)(self.wrapped.CompoundModalAnalysis) if self.wrapped.CompoundModalAnalysis else None

    @property
    def compound_dynamic_analysis(self) -> '_2338.CompoundDynamicAnalysis':
        '''CompoundDynamicAnalysis: 'CompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2338.CompoundDynamicAnalysis)(self.wrapped.CompoundDynamicAnalysis) if self.wrapped.CompoundDynamicAnalysis else None

    @property
    def compound_critical_speed_analysis(self) -> '_2337.CompoundCriticalSpeedAnalysis':
        '''CompoundCriticalSpeedAnalysis: 'CompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2337.CompoundCriticalSpeedAnalysis)(self.wrapped.CompoundCriticalSpeedAnalysis) if self.wrapped.CompoundCriticalSpeedAnalysis else None

    @property
    def compound_stability_analysis(self) -> '_2352.CompoundStabilityAnalysis':
        '''CompoundStabilityAnalysis: 'CompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2352.CompoundStabilityAnalysis)(self.wrapped.CompoundStabilityAnalysis) if self.wrapped.CompoundStabilityAnalysis else None

    @property
    def compound_modal_analysis_at_a_speed(self) -> '_2347.CompoundModalAnalysisAtASpeed':
        '''CompoundModalAnalysisAtASpeed: 'CompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2347.CompoundModalAnalysisAtASpeed)(self.wrapped.CompoundModalAnalysisAtASpeed) if self.wrapped.CompoundModalAnalysisAtASpeed else None

    @property
    def compound_modal_analysis_at_a_stiffness(self) -> '_2348.CompoundModalAnalysisAtAStiffness':
        '''CompoundModalAnalysisAtAStiffness: 'CompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2348.CompoundModalAnalysisAtAStiffness)(self.wrapped.CompoundModalAnalysisAtAStiffness) if self.wrapped.CompoundModalAnalysisAtAStiffness else None

    @property
    def compound_torsional_system_deflection(self) -> '_2357.CompoundTorsionalSystemDeflectionAnalysis':
        '''CompoundTorsionalSystemDeflectionAnalysis: 'CompoundTorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2357.CompoundTorsionalSystemDeflectionAnalysis)(self.wrapped.CompoundTorsionalSystemDeflection) if self.wrapped.CompoundTorsionalSystemDeflection else None

    @property
    def compound_harmonic_analysis_of_single_excitation(self) -> '_2345.CompoundHarmonicAnalysisOfSingleExcitationAnalysis':
        '''CompoundHarmonicAnalysisOfSingleExcitationAnalysis: 'CompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2345.CompoundHarmonicAnalysisOfSingleExcitationAnalysis)(self.wrapped.CompoundHarmonicAnalysisOfSingleExcitation) if self.wrapped.CompoundHarmonicAnalysisOfSingleExcitation else None

    @property
    def compound_advanced_system_deflection_sub_analysis(self) -> '_2335.CompoundAdvancedSystemDeflectionSubAnalysis':
        '''CompoundAdvancedSystemDeflectionSubAnalysis: 'CompoundAdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2335.CompoundAdvancedSystemDeflectionSubAnalysis)(self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis) if self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis else None

    @property
    def compound_dynamic_model_for_harmonic_analysis(self) -> '_2340.CompoundDynamicModelForHarmonicAnalysis':
        '''CompoundDynamicModelForHarmonicAnalysis: 'CompoundDynamicModelForHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2340.CompoundDynamicModelForHarmonicAnalysis)(self.wrapped.CompoundDynamicModelForHarmonicAnalysis) if self.wrapped.CompoundDynamicModelForHarmonicAnalysis else None

    @property
    def compound_dynamic_model_for_stability_analysis(self) -> '_2341.CompoundDynamicModelForStabilityAnalysis':
        '''CompoundDynamicModelForStabilityAnalysis: 'CompoundDynamicModelForStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2341.CompoundDynamicModelForStabilityAnalysis)(self.wrapped.CompoundDynamicModelForStabilityAnalysis) if self.wrapped.CompoundDynamicModelForStabilityAnalysis else None

    @property
    def compound_dynamic_model_at_a_stiffness(self) -> '_2339.CompoundDynamicModelAtAStiffnessAnalysis':
        '''CompoundDynamicModelAtAStiffnessAnalysis: 'CompoundDynamicModelAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2339.CompoundDynamicModelAtAStiffnessAnalysis)(self.wrapped.CompoundDynamicModelAtAStiffness) if self.wrapped.CompoundDynamicModelAtAStiffness else None

    @property
    def compound_dynamic_model_for_steady_state_synchronous_response(self) -> '_2342.CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis':
        '''CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis: 'CompoundDynamicModelForSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2342.CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundDynamicModelForSteadyStateSynchronousResponse) if self.wrapped.CompoundDynamicModelForSteadyStateSynchronousResponse else None

    @property
    def compound_modal_analysis_for_harmonic_analysis(self) -> '_2349.CompoundModalAnalysisForHarmonicAnalysis':
        '''CompoundModalAnalysisForHarmonicAnalysis: 'CompoundModalAnalysisForHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2349.CompoundModalAnalysisForHarmonicAnalysis)(self.wrapped.CompoundModalAnalysisForHarmonicAnalysis) if self.wrapped.CompoundModalAnalysisForHarmonicAnalysis else None

    @property
    def compound_advanced_time_stepping_analysis_for_modulation(self) -> '_2336.CompoundAdvancedTimeSteppingAnalysisForModulation':
        '''CompoundAdvancedTimeSteppingAnalysisForModulation: 'CompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2336.CompoundAdvancedTimeSteppingAnalysisForModulation)(self.wrapped.CompoundAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.CompoundAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def compound_harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(self) -> '_2344.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation':
        '''CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation: 'CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2344.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation)(self.wrapped.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation else None

    def create_load_cases(self, number_of_load_cases: 'int', token: '_7202.TaskProgress') -> 'List[_6447.LoadCase]':
        ''' 'CreateLoadCases' is the original name of this method.

        Args:
            number_of_load_cases (int)
            token (mastapy.TaskProgress)

        Returns:
            List[mastapy.system_model.analyses_and_results.static_loads.LoadCase]
        '''

        number_of_load_cases = int(number_of_load_cases)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.CreateLoadCases(number_of_load_cases if number_of_load_cases else 0, token.wrapped if token else None), constructor.new(_6447.LoadCase))

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

    def analysis_of(self, analysis_type: '_6459.AnalysisType') -> '_2296.CompoundAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.CompoundAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
