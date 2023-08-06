'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._904 import ZerolBevelGearDesign
    from ._905 import ZerolBevelGearMeshDesign
    from ._906 import ZerolBevelGearSetDesign
    from ._907 import ZerolBevelMeshedGearDesign
