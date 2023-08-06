'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._883 import ZerolBevelGearDesign
    from ._884 import ZerolBevelGearMeshDesign
    from ._885 import ZerolBevelGearSetDesign
    from ._886 import ZerolBevelMeshedGearDesign
