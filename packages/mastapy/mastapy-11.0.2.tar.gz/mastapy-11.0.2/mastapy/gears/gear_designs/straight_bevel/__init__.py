'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._896 import StraightBevelGearDesign
    from ._897 import StraightBevelGearMeshDesign
    from ._898 import StraightBevelGearSetDesign
    from ._899 import StraightBevelMeshedGearDesign
