from django.core.exceptions import ValidationError
from django.db import models


def validate_positive_value(value):
    if value <= 0:
        raise ValidationError("Значение должно быть больше 0.")


class Client(models.Model):
    username = models.CharField(verbose_name="Логин клиента", max_length=100)

    def __str__(self):
        return self.username


class Item(models.Model):
    name = models.CharField(verbose_name="Наименование товара", max_length=100)
    price = models.FloatField(
        verbose_name="Стоимость товара", validators=[validate_positive_value]
    )

    def __str__(self):
        return self.name


class Deal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="deals")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="deals")
    total = models.FloatField(
        verbose_name="Сумма сделки", validators=[validate_positive_value]
    )
    quantity = models.IntegerField(
        verbose_name="Количество товара", validators=[validate_positive_value]
    )
    date_time = models.DateTimeField(verbose_name="Дата и время регистрации сделки")

    def __str__(self):
        return f"{self.client} {self.item}"
