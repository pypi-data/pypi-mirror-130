'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._908 import WormDesign
    from ._909 import WormGearDesign
    from ._910 import WormGearMeshDesign
    from ._911 import WormGearSetDesign
    from ._912 import WormWheelDesign
