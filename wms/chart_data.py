import datetime
import sqlalchemy
from sqlalchemy import Table, MetaData, select, and_
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base



engine = sqlalchemy.create_engine('oracle://web:oracle@wmsdb11')
Base = declarative_base()
metadata = MetaData(bind=engine)

class Charts(Base):
    __table__ = Table('wms_charts', metadata, autoload=True)

    @staticmethod
    def get_chart_description(chart_id):
        session = create_session(bind=engine)
        current_chart = session.query(Charts).filter(Charts.id == chart_id).one()
        session.close()
        return (current_chart.__dict__)

def get_chart_data(current_chart, date_start, date_end):
    session = create_session(bind=engine)
    chart_data_object = Table(current_chart['view_name'], metadata, autoload=True)

    chart_data={}
    chart_name = current_chart['chart_name']
    chart_date_field = getattr(chart_data_object.c, current_chart['x_axis_field'])
    chart_value_field = getattr(chart_data_object.c, current_chart['y_axis_field'])



    query_data =  session.execute(select([chart_date_field, chart_value_field]).\
                    where(and_(chart_date_field < date_end, chart_date_field > date_start)).\
                    order_by(chart_date_field)).\
                    fetchall()

    chart_data[chart_name] = {}
    chart_data[chart_name]['dates'] = []
    chart_data[chart_name]['values'] = []

    for dates, values in query_data:
        print('Building up chart_data')
        chart_data[chart_name]['dates'].append(datetime.datetime.strptime(dates, '%d.%m.%y').strftime('%d %b %Y'))
        chart_data[chart_name]['values'].append(values)

    return chart_data