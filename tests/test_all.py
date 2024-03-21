import image_comparison as ic


def test_import():
    assert ic.__version__
    assert ic.version_info
    assert ic.compare_images
