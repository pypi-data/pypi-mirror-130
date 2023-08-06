'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._917 import StraightBevelGearDesign
    from ._918 import StraightBevelGearMeshDesign
    from ._919 import StraightBevelGearSetDesign
    from ._920 import StraightBevelMeshedGearDesign
