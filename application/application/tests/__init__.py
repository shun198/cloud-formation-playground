import os

if os.environ.get("CI_MAKING_DOCS") is not None:
    """テスト仕様書をpdocで出力するためにdjango.setupを実施する"""
    import django

    django.setup()
