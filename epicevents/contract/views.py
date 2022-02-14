from rest_framework import viewsets
from .serializers import ContractSerializer
from .models import Contract
from event.models import Event
from users.models import EpicUser as User
from account.models import Account
from epicevents.permissions import IsSales
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("contract.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsSales]
    http_method_names = ["get", "patch", "post"]
    filterset_fields = [
        "account__last_name",
        "account__email",
        "date_created",
        "amount",
    ]
    search_fields = ["account__last_name", "account__email", "date_created", "amount"]
    logger.info("ContractViewSet allowed HTTP methods {}".format(http_method_names))

    def get_queryset(self):
        return Contract.objects.filter(sales_contact=self.request.user).order_by("id")

    def update(self, request, *args, **kwargs):
        contract = Contract.objects.get(pk=self.kwargs["pk"])
        if contract.sales_contact.id == request.user.id and request.POST["status"]:
            Event.objects.create(account=contract.account)
        if contract.sales_contact.id == request.user.id:
            serializer = self.get_serializer(contract, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            raise PermissionDenied

    def create(self, request):
        account = Account.objects.get(pk=request.POST["account"])
        if account.sales_contact == request.user:
            user = User.objects.get(pk=request.user.id)
            contract = Contract.objects.create(
                account=account,
                sales_contact=user,
                payment_due=request.POST["payment_due"],
            )
            serializer = self.get_serializer(contract)

            return Response(serializer.data)
        else:
            raise PermissionDenied
