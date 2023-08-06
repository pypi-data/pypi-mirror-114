'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2024 import ClutchConnection
    from ._2025 import ClutchSocket
    from ._2026 import ConceptCouplingConnection
    from ._2027 import ConceptCouplingSocket
    from ._2028 import CouplingConnection
    from ._2029 import CouplingSocket
    from ._2030 import PartToPartShearCouplingConnection
    from ._2031 import PartToPartShearCouplingSocket
    from ._2032 import SpringDamperConnection
    from ._2033 import SpringDamperSocket
    from ._2034 import TorqueConverterConnection
    from ._2035 import TorqueConverterPumpSocket
    from ._2036 import TorqueConverterTurbineSocket
