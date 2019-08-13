from django.db.models import Q, F, Avg

__author__ = 'R.Azh'

import datetime

start_date = datetime.date(2017, 9, 20)
end_date = datetime.date(2017, 12,20 )

MonitoringResult.objects.all().filter(
        (
            Q(timestamp__lt=end_date) &
            Q(timestamp__gt=start_date)
        )
).values(  # GROUP BY
    'value',
).aggregate(
    Avg('value')
)

from django.db.models import Subquery
start_time = datetime.datetime.utcnow()
result = []
links = Link.objects.filter(link_type=1)
for link in links:
    kpis = Kpi.objects.filter(link=link).values('pk') #.values('pk', 'kpi_type')

    # print(MonitoringResult.objects.filter(
    #                        Q(timestamp__lt=end_date) &
    #                        Q(timestamp__gt=start_date),
    #                           kpi__in=Subquery(kpis),
    #
    #            ).count())

    avg = MonitoringResult.objects.filter(
                     Q(timestamp__lt=end_date) &
                     Q(timestamp__gt=start_date),
                       kpi__in=Subquery(kpis),

         ).values(  # GROUP BY
             'kpi__kpi_type',
         ).annotate(
             Avg('value')
    )
    result.append({'link': link, 'avg': avg})
print(datetime.datetime.utcnow()-start_time)
print(result)



kpis = Kpi.objects.filter(link=links[10]).values('kpi_type').annotate(average=Avg('pk'))






# ExchangeRate.objects.all().filter(
#         (
#             Q(start_date__lt=start_date) &
#             Q(end_date__gt=start_date)
#         ) | (
#             Q(start_date__gte=start_date) &
#             Q(start_date__lt=end_date) &
#             Q(end_date__gt=start_date)
#         )
# ).annotate(
#     currency_from_name = 'currency_from__name',
#     currency_to_name = 'currency_to__name'
# ).values(  # GROUP BY
#     'currency_from_name',
#     'currency_to_name'
# ).aggregate(
#     F('currency_from_name'),
#     F('currency_to_name'),
#     Avg('exchange_rate')
# )

from django.db.models import OuterRef, Subquery, Sum
comments = Comment.objects.filter(post=OuterRef('pk')).order_by().values('post')
total_comments = comments.annotate(total=Sum('length')).values('total')
Post.objects.filter(length__gt=Subquery(total_comments))