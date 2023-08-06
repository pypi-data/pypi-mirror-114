'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1089 import ConceptGearDesign
    from ._1090 import ConceptGearMeshDesign
    from ._1091 import ConceptGearSetDesign
