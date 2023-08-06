'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._925 import KlingelnbergCycloPalloidSpiralBevelGearDesign
    from ._926 import KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
    from ._927 import KlingelnbergCycloPalloidSpiralBevelGearSetDesign
    from ._928 import KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
