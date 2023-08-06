'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2164 import ConcentricOrParallelPartGroup
    from ._2165 import ConcentricPartGroup
    from ._2166 import ConcentricPartGroupParallelToThis
    from ._2167 import DesignMeasurements
    from ._2168 import ParallelPartGroup
    from ._2169 import PartGroup
