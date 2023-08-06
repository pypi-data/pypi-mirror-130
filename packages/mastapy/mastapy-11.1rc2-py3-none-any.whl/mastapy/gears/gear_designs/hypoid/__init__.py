'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._937 import HypoidGearDesign
    from ._938 import HypoidGearMeshDesign
    from ._939 import HypoidGearSetDesign
    from ._940 import HypoidMeshedGearDesign
