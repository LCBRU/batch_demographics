from flask import flash
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, SelectField
from wtforms.fields import FieldList, FormField
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField, FileRequired
from batch_demographics.model import Column


class FlashingForm(FlaskForm):
    def validate_on_submit(self):
        result = super(FlashingForm, self).validate_on_submit()

        if not result:
            for field, errors in self.errors.items():
                for error in errors:
                    flash(
                        "Error in the {} field - {}".format(
                            getattr(self, field).label.text, error
                        ), 'error')
        return result


class SearchForm(FlashingForm):
    search = StringField("Search", validators=[Length(max=20)])
    page = IntegerField("Page", default=1)


class ConfirmForm(FlashingForm):
    id = HiddenField("id")


class BatchForm(FlashingForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    participant_file = FileField('Participants File', validators=[FileRequired()])


class MappingForm(FlaskForm):
    column_id = HiddenField('column_id')
    column_name = HiddenField('column_name')
    mapping = SelectField('Mapping', choices=Column.get_select_options())


class MappingsForm(FlaskForm):
    column_mappings = FieldList(FormField(MappingForm))
