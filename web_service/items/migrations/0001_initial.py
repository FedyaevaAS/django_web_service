import django.db.models.deletion
import items.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=100, verbose_name="Логин клиента"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Наименование товара"
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        validators=[items.models.validate_positive_value],
                        verbose_name="Стоимость товара",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Deal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total",
                    models.FloatField(
                        validators=[items.models.validate_positive_value],
                        verbose_name="Сумма сделки",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[items.models.validate_positive_value],
                        verbose_name="Количество товара",
                    ),
                ),
                (
                    "date_time",
                    models.DateTimeField(
                        verbose_name="Дата и время регистрации сделки"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deals",
                        to="items.client",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deals",
                        to="items.item",
                    ),
                ),
            ],
        ),
    ]
