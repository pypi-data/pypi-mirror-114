'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._887 import WormDesign
    from ._888 import WormGearDesign
    from ._889 import WormGearMeshDesign
    from ._890 import WormGearSetDesign
    from ._891 import WormWheelDesign
