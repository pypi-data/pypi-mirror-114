'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1203 import KeyedJointDesign
    from ._1204 import KeyTypes
    from ._1205 import KeywayJointHalfDesign
    from ._1206 import NumberOfKeys
