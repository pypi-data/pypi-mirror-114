'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2288 import ActiveFESubstructureSelection
    from ._2289 import ActiveFESubstructureSelectionGroup
    from ._2290 import ActiveShaftDesignSelection
    from ._2291 import ActiveShaftDesignSelectionGroup
    from ._2292 import BearingDetailConfiguration
    from ._2293 import BearingDetailSelection
    from ._2294 import PartDetailConfiguration
    from ._2295 import PartDetailSelection
