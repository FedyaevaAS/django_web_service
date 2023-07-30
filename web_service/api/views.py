import csv
import io
from datetime import datetime

from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from items.models import Client, Deal, Item
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class FileUploadView(APIView):
    def post(self, request):
        try:
            file = request.data["file"]
            file_extension = file.name.split(".")[-1].lower()
            if file_extension != "csv":
                return Response(
                    {"error": "Некорректный формат файла"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            decoded_file = file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            for row in reader:
                self.create_deal(row)
            return Response(
                {"message": "Данные успешно загружены"},
                status=status.HTTP_201_CREATED,
            )
        except KeyError as e:
            key = e.args[0]
            if key == "file":
                error = "Файл не найден"
            else:
                error = f"Колонка {key} отсутствует в CSV файле"
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create_deal(self, row):
        username = row["customer"]
        item_name = row["item"]
        total = row["total"]
        quantity = row["quantity"]
        date_time = datetime.strptime(row["date"], DATETIME_FORMAT)
        client, created = Client.objects.get_or_create(username=username)
        price = int(total) / int(quantity)
        item, created = Item.objects.get_or_create(name=item_name, price=price)
        aware_date_time = timezone.make_aware(date_time, timezone.utc)
        Deal.objects.get_or_create(
            client=client,
            item=item,
            total=total,
            quantity=quantity,
            date_time=aware_date_time,
        )


class TopClientsView(APIView):
    CACHE_TIMEOUT = 60

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def get(self, request):
        top_clients = Client.objects.annotate(spent_money=Sum("deals__total")).order_by(
            "-spent_money"
        )[:5]
        top_clients_deals = Deal.objects.filter(client__in=top_clients)
        gems_list = (
            top_clients_deals.values("item__name")
            .annotate(client_count=Count("client", distinct=True))
            .filter(client_count__gte=2)
            .values_list("item__name", flat=True)
        )
        top_clients_data = [
            {
                "username": client.username,
                "spent_money": client.spent_money,
                "gems": self.get_client_gems(client, gems_list),
            }
            for client in top_clients
        ]

        return Response({"response": top_clients_data}, status=status.HTTP_200_OK)

    def get_client_gems(self, client, gems_list):
        client_items = client.deals.values_list("item__name", flat=True).distinct()
        return [client_item for client_item in client_items if client_item in gems_list]
