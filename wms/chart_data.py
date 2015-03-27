import datetime
import sqlalchemy, sys
from sqlalchemy import Table, MetaData, func, select, and_
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

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
        print(chart_type_names)

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
        charts = session.query(Charts)
        for chart_name in charts:
            chart_description['chart_id'] = chart_name.id
            chart_description['chart_type_id'] = chart_name.chart_type_id
            chart_description['chart_type_name'] = chart_type_names[chart_name.chart_type_id]
            chart_names.append((chart_description, chart_name.chart_name))
        session.close()
        print(chart_names)

        return chart_names

#Building data for charts
def get_chart_data(current_chart, date_start, date_end):
    session = create_session(bind=engine)
    chart_data_object = Table(current_chart['view_name'], metadata, autoload=True)

    chart_data={}
    chart_name = current_chart['chart_name']
    chart_date_field = getattr(chart_data_object.c, current_chart['x_axis_field'])
    chart_value_field = getattr(chart_data_object.c, current_chart['y_axis_field'])

    try:
        query_data =  session.execute(select([chart_date_field, chart_value_field]).\
                    where(and_(chart_date_field < date_end, chart_date_field > date_start)).\
                    order_by(chart_date_field)).\
                    fetchall()
    except:
        print(sys.exc_info())
    print('bbb')

    query_data =  session.execute(select([chart_date_field, func.sum(chart_value_field), chart_group_field]).\
                    group_by(chart_group_field, chart_date_field).\
                    order_by(chart_group_field, chart_date_field)).\
                    fetchall()

    chart_data[chart_name] = {}
    chart_data[chart_name]['dates'] = []
    chart_data[chart_name]['values'] = []

    for dates, values in query_data:
        print('Building up chart_data')
        chart_data[chart_name]['dates'].append(dates.strftime('%d %b %Y'))
        chart_data[chart_name]['values'].append(values)

    return chart_data