'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._933 import KlingelnbergConicalGearDesign
    from ._934 import KlingelnbergConicalGearMeshDesign
    from ._935 import KlingelnbergConicalGearSetDesign
    from ._936 import KlingelnbergConicalMeshedGearDesign
