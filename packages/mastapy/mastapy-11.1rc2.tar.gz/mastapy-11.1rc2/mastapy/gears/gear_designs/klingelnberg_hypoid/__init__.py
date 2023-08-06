'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._929 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._930 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._931 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._932 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
