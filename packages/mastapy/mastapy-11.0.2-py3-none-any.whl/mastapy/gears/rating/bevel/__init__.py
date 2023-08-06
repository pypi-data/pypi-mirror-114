'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._503 import BevelGearMeshRating
    from ._504 import BevelGearRating
    from ._505 import BevelGearSetRating
