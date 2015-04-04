import datetime, calendar
import sqlalchemy, sys
from sqlalchemy import Table, MetaData, func, select, text, literal_column, bindparam, and_
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from collections import defaultdict
from itertools import groupby

engine = sqlalchemy.create_engine('oracle://web:oracle@wmsdb11')
Base = declarative_base()
metadata = MetaData(bind=engine)

class ChartType(Base):
    __table__ = Table('wms_charttype', metadata, autoload=True)

    @staticmethod
    def get_chart_type_name(chart_type_id):
        session = create_session(bind=engine)
        chart_type_name = session.query(ChartType).filter(ChartType.id == chart_type_id).one()
        session.close()

        return chart_type_name.type

    @staticmethod
    #List of available chart types
    def get_all_chart_type_names():
        print('Getting list of chart types')
        chart_type_names={}
        session = create_session(bind =engine)
        chart_types= session.query(ChartType)
        for chart_type in chart_types:
            chart_type_names[chart_type.id] = chart_type.type
        session.close()
        print(sys._getframe().f_code.co_name + ': Chart type names: ' + str(chart_type_names))

        return chart_type_names


class Charts(Base):
    __table__ = Table('wms_charts', metadata, autoload=True)

    @staticmethod
    #Fetching chart object. Currently used only for fetching data for chart rendering
    def get_chart_description(chart_id):
        session = create_session(bind=engine)
        current_chart = session.query(Charts).filter(Charts.id == chart_id).one()
        session.close()

        return (current_chart.__dict__)

    @staticmethod
    #Fetching all chart names for filling chart form in web
    def get_chart_names():
        chart_description={}
        chart_names = []
        chart_type_names = ChartType.get_all_chart_type_names()

        session = create_session(bind=engine)
        charts = session.query(Charts).all()
        for chart_name in charts:
            chart_description['chart_id'] = chart_name.id
            chart_description['chart_type_id'] = chart_name.chart_type_id
            chart_description['chart_type_name'] = chart_type_names[chart_name.chart_type_id]
            chart_names.append((chart_description, chart_name.chart_name))
            #fix so chart_names won't get the same chart_description for all charts, with the values from the last chart
            chart_description={}
        session.close()
        print(sys._getframe().f_code.co_name + ': Chart types:')
        print(chart_names)

        return chart_names

def generate_select(chart_date_field, chart_value_field, chart_group_field, date_start, date_end):
    print(sys._getframe().f_code.co_name + ': Generating simple select statement')
    #'bindparam' is used to unify the code later. Grants ability to use single 'build_up_chart_data' function for both
    #single and grouped selects ('build_up_grouped_chart_data' function is deprecated now)
    selection = select([chart_date_field, chart_value_field, bindparam("grouping_field", chart_group_field)]).\
        where(and_(chart_date_field <= date_end, chart_date_field >= date_start)).\
        order_by(chart_date_field)
    return selection

def generate_grouped_select(chart_date_field, chart_value_field, chart_sum_field, chart_group_field, date_start,
                            date_end):
    print(sys._getframe().f_code.co_name + ': Generating select statement with grouping')
    selection = select([chart_date_field, func.sum(chart_value_field).label(chart_sum_field), chart_group_field]).\
        where(and_(chart_date_field <= date_end, chart_date_field >= date_start)).\
        group_by(chart_group_field, chart_date_field).\
        order_by(chart_group_field, chart_date_field)
    return selection

#Building data for charts
def get_chart_data(current_chart, date_start, date_end, interval_type):
    print(current_chart)
    session = create_session(bind=engine)
    chart_data_object = Table(current_chart['view_name'], metadata, autoload=True)

    chart_date_field = getattr(chart_data_object.c, current_chart['x_axis_field'])
    chart_value_field = getattr(chart_data_object.c, current_chart['y_axis_field'])

    #Prepare select statement depending on chart's grouping flag
    print(sys._getframe().f_code.co_name + ': Determine select handling type')
    if str2bool(current_chart['grouping']):
        grouping_field = current_chart['grouping_field']
        chart_sum_field = current_chart['y_axis_field']
        chart_group_field = getattr(chart_data_object.c, grouping_field)
        selection = generate_grouped_select(chart_date_field, chart_value_field, chart_sum_field, chart_group_field,
                                            date_start, date_end)
    else:
        chart_group_field = current_chart['chart_name']
        selection = generate_select(chart_date_field, chart_value_field, chart_group_field, date_start, date_end)
    print('Select statement:\n' + str(selection))

    #Fetch data for DB using select statement from section above
    try:
        query_data = session.execute(selection).fetchall()
    except:
        print(sys.exc_info())

    print(query_data)
    group_by_interval = (interval_type != 'day')

    #Prepare data for chart based on results of DB query
    chart_data = build_up_chart_data(query_data, group_by_interval)

    print(interval_type)

    #Checking whether data needs to be grouped by selected interval
    if group_by_interval:
        try:
            chart_data = build_up_chart_data_by_interval(chart_data, interval_type)
        except:
            print('Failed to group by interval')
            print(sys.exc_info())

    print(sys._getframe().f_code.co_name + ': Chart data will be:')
    print(chart_data)
    return chart_data

#Function to prepare data for chart. This data can be grouped up by interval later, hence 'group_by_interval' parameter.
#If data will be grouped by interval later then 'dates' list need to be filled only with datetime type
#else 'dates' are converted to human-readable format to display on the chart y-axis
def build_up_chart_data(query_data, group_by_interval):
    chart_data = defaultdict(lambda: defaultdict(list))
    if group_by_interval:
        for dates, values, group in query_data:
            chart_data[group]['dates'].append(dates)
            chart_data[group]['values'].append(values)
    else:
        for dates, values, group in query_data:
            chart_data[group]['dates'].append(dates.strftime('%d %b'))
            chart_data[group]['values'].append(values)
    return chart_data

#Not in use, to be removed soon. Unified code
# def build_up_grouped_chart_data(query_data):
#     chart_data = defaultdict(lambda: defaultdict(list))
#     for dates, values, group in query_data:
#         chart_data[group]['dates'].append(dates.strftime('%d %b'))
#         chart_data[group]['values'].append(values)
#     return chart_data

def build_up_chart_data_by_interval(query_data, interval_type):
    chart_data = defaultdict(lambda: defaultdict(list))
    def grouper(item):
        if interval_type == 'week':
            return item.isocalendar()[1]
        else:
            return getattr(item,interval_type)

    res = 0
    for key in query_data:
        for (grouping_type, group) in groupby(query_data[key]['dates'], grouper):
            for item in group:
                item_index = query_data[key]['dates'].index(item)
                res += query_data[key]['values'][item_index]
            chart_data[key]['dates'].append(date_format(item,interval_type))
            chart_data[key]['values'].append(res)
            res = 0
    print(chart_data)
    return chart_data


def date_format(date, format):
    date_formatted = date
    if format == 'week':
        date_formatted = 'Week ' + str(date_formatted.isocalendar()[1])
    elif format == 'month':
        date_formatted = date_formatted.strftime('%b %y')
    elif format == 'year':
        date_formatted = date_formatted.strftime('%Y')
    return date_formatted

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

