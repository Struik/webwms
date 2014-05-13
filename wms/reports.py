import datetime, qsstats
from wms.models import Order, OrderDetail, Incoming, IncomingDetail
from qsstats import QuerySetStats
from django.db.models import Count
from collections import defaultdict

class ChartData(object):

    @classmethod
    def documents_over_period(cls, chart_params):
        print('111')
        today = datetime.date.today().strftime('%d.%m.%Y')
        start_date = datetime.datetime.strptime(chart_params['start_date'][0] or (today), '%d.%m.%Y')
        end_date = datetime.datetime.strptime(chart_params['end_date'][0] or (today), '%d.%m.%Y')
        document_stats={}
        data = defaultdict()

        print(chart_params)

        for document in chart_params['documents']:
            if document == 'Order':
                queryset = Order.objects.all()
            elif document == 'Incoming':
                queryset = Incoming.objects.all()

            qsstats = QuerySetStats(queryset, date_field='date_to_ship', aggregate=Count('id'))
            document_stats[document] = qsstats.time_series(start_date, end_date, interval='days')

            data[document] = {'dates': [], 'values': []}
            for item in document_stats[document]:
                data[document]['dates'].append(item[0].strftime('%d %b'))
                data[document]['values'].append(item[1])

        return data