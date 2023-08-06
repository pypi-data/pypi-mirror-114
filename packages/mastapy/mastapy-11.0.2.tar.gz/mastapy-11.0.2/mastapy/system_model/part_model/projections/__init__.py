'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2162 import SpecifiedConcentricPartGroupDrawingOrder
    from ._2163 import SpecifiedParallelPartGroupDrawingOrder
