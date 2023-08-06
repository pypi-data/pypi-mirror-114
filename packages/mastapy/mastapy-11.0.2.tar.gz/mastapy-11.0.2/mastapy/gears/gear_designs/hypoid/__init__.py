'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._916 import HypoidGearDesign
    from ._917 import HypoidGearMeshDesign
    from ._918 import HypoidGearSetDesign
    from ._919 import HypoidMeshedGearDesign
