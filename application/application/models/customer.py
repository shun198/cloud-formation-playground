import uuid

from django.core.validators import RegexValidator
from django.db import models

from application.utils.customer_storage import CustomerStorage


class Customer(models.Model):
    """お客様"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="お客様ID",
    )
    kana = models.CharField(
        max_length=255,
        db_comment="カナ氏名",
    )
    name = models.CharField(
        max_length=255,
        db_comment="氏名",
    )
    birthday = models.DateField(
        db_comment="誕生日",
    )
    phone_no = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^[0-9]{11}$", "11桁の数字を入力してください。")],
        blank=True,
        db_comment="電話番号",
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="address",
        db_comment="住所ID",
    )

    class Meta:
        db_table = "Customer"
        db_table_comment = "お客様"


class CustomerPhoto(models.Model):
    """お客様の画像"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="お客様の写真ID",
    )
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        db_comment="お客様ID",
    )
    photo = models.ImageField(
        upload_to="customer_photo",
        storage=CustomerStorage(),
        db_comment="写真",
    )

    class Meta:
        db_table = "CustomerPhoto"
        db_table_comment = "お客様の画像"


class Address(models.Model):
    """住所"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="住所ID",
    )
    prefecture = models.CharField(
        max_length=255,
        db_comment="都道府県",
    )
    municipalities = models.CharField(
        max_length=255,
        db_comment="市区町村",
    )
    house_no = models.CharField(
        max_length=255,
        db_comment="丁・番地",
    )
    other = models.CharField(
        max_length=255,
        blank=True,
        db_comment="その他(マンション名など)",
    )
    post_no = models.CharField(
        max_length=7,
        validators=[RegexValidator(r"^[0-9]{7}$", "7桁の数字を入力してください。")],
        null=True,
        db_comment="郵便番号",
    )

    class Meta:
        db_table = "Address"
        db_table_comment = "住所"
