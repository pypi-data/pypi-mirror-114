'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._875 import DesignConstraint
    from ._876 import DesignConstraintCollectionDatabase
    from ._877 import DesignConstraintsCollection
    from ._878 import GearDesign
    from ._879 import GearDesignComponent
    from ._880 import GearMeshDesign
    from ._881 import GearSetDesign
    from ._882 import SelectedDesignConstraintsCollection
