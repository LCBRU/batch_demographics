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


class MappingsForm(FlashingForm):
    column_mappings = FieldList(FormField(MappingForm))

    def validate(self):
        if not FlashingForm.validate(self):
            return False

        result = True
        seen = {}

        for cm in self.column_mappings.entries:
            if not cm.mapping.data:
                continue

            if cm.mapping.data in seen.keys():
                seen[cm.mapping.data].append(cm)
            else:
                seen[cm.mapping.data] = [cm]

        for mapping, usage in seen.items():
            if len(usage) > 1:
                message = "'{}' has been used multiple times for the following fields: '{}'.".format(
                    mapping, ', '.join(u.column_name.data for u in usage))

                for u in usage:
                    u.mapping.errors.append(message)

                flash(message, "error")
                result = False

        return result
