# -*- coding: utf-8 -*-
import itertools
import datetime
from django import forms
from wms.models import ChartType
 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%I:%M %p'


class ChartForm(forms.Form):

    start_date = forms.DateField(label='С', required=False, input_formats=[DATE_FORMAT])
    end_date = forms.DateField(label='По', required=False, input_formats=[DATE_FORMAT])

    documents = forms.MultipleChoiceField(
        label='Документы',
        required=False,
        choices = (
            ('Order', "Заказы"),
            ('Incoming', 'Поставки'),
            # ('OrderDetail', "Строки заказов"),
            # ('IncomingDetail', 'Строки поставок'),
        ),
        initial = 'option_one', widget = forms.CheckboxSelectMultiple, help_text = "Отметьте документы для отображения",
    )

    def __init__(self, *args, **kwargs):
        super(ChartForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'add_chart'
        self.helper.form_method = 'get'

        self.fields['start_date'].initial = datetime.date.today().strftime(DATE_FORMAT)
        self.fields['end_date'].initial = datetime.date.today().strftime(DATE_FORMAT)

        self.fields['chart_type'] = forms.ChoiceField(
            label='Тип графика',
            choices = self.get_chart_types(ChartType.objects.all()),
            required=False)

        self. helper.layout = Layout(
            Field('chart_type', css_class='input_sm'),
            Field('start_date', placeholder='From (mm.dd.yyyy)',),
            Field('end_date', placeholder='To (mm.dd.yyyy)', ),
            Field('documents',),
            FormActions(
                Submit('submit', 'Построить', css_class="btn-success btn-xs"),
                Reset('reset', 'Сбросить', css_class="btn-default btn-xs"),
                Button('add', 'Добавить', css_class="btn-primary btn-xs"),
            ),
        )

    def get_chart_types(self, queryset):
        choices = [('', '---')] +list([(i.type, i.label) for i in queryset])
        return choices



class MessageForm(forms.Form):
    text_input = forms.CharField()
 
    textarea = forms.CharField(
        widget = forms.Textarea(),
    )
 
    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )
 
    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )
 
    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )
 
    prepended_text = forms.CharField()
 
    prepended_text_two = forms.CharField()
 
    multicolon_select = forms.ChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )
 
    #Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )
