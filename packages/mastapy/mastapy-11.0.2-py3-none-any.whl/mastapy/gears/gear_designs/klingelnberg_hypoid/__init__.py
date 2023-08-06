'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._908 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._909 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._910 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._911 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
