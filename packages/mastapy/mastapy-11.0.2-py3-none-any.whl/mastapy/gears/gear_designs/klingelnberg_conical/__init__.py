'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._912 import KlingelnbergConicalGearDesign
    from ._913 import KlingelnbergConicalGearMeshDesign
    from ._914 import KlingelnbergConicalGearSetDesign
    from ._915 import KlingelnbergConicalMeshedGearDesign
