from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, OuterRef, Subquery, DateField
from django.db.models.functions import Cast
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema

from bookings.models import Booking, RecurringActivityBooking, OneTimeActivityBooking

from .serializers import RequestStatSerializer, ResponseStatSerializer


@extend_schema(parameters=[RequestStatSerializer], responses=ResponseStatSerializer)
class StatView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        serializer = RequestStatSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        current_user = request.user
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]
        trunc_func = serializer.get_trunc_function()

        stats = self.get_stats(current_user, start, end, trunc_func)
        serializer = ResponseStatSerializer(stats, many=True)

        return Response(serializer.data)

    def get_stats(self, user, start, end, trunc_func):
        recurring_type = ContentType.objects.get_for_model(RecurringActivityBooking).id
        one_time_type = ContentType.objects.get_for_model(OneTimeActivityBooking).id

        bookings = Booking.objects.filter(
            activity__created_by=user, booked_at__range=(start, end)
        ).annotate(period=Cast(trunc_func("booked_at"), output_field=DateField()))

        customers = bookings.values("period", "booked_by").annotate(count=Count("id"))

        stats = (
            bookings.values("period")
            .annotate(
                total_bookings=Count("id"),
                recurring_activity_bookings=Count(
                    "id", filter=Q(polymorphic_ctype_id=recurring_type)
                ),
                one_time_activity_bookings=Count(
                    "id", filter=Q(polymorphic_ctype_id=one_time_type)
                ),
                total_customers=Count("booked_by", distinct=True),
                repeat_customers=Count(
                    "booked_by",
                    filter=Q(
                        booked_by__in=Subquery(
                            customers.filter(
                                period=OuterRef("period"), count__gt=1
                            ).values("booked_by")
                        )
                    ),
                    distinct=True,
                ),
            )
            .order_by("period")
        )
        return list(stats)
