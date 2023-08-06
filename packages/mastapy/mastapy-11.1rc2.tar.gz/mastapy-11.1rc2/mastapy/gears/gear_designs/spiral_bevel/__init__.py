'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._921 import SpiralBevelGearDesign
    from ._922 import SpiralBevelGearMeshDesign
    from ._923 import SpiralBevelGearSetDesign
    from ._924 import SpiralBevelMeshedGearDesign
