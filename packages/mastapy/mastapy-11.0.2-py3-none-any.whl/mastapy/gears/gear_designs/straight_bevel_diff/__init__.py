'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._892 import StraightBevelDiffGearDesign
    from ._893 import StraightBevelDiffGearMeshDesign
    from ._894 import StraightBevelDiffGearSetDesign
    from ._895 import StraightBevelDiffMeshedGearDesign
