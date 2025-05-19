from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLForm(FlaskForm):
    original_link = StringField('Длинная ссылка',
                                validators=[
                                    DataRequired(message='Обязательное поле'),
                                    Length(1, 512),
                                    URL(message='Некорректная ссылка')
                                ])
    custom_id = StringField('Короткая ссылка',
                            validators=[
                                Optional(),
                                Length(min=1, max=16,
                                       message='Длина ссылки должна'
                                               ' быть от 1 до 16 символов'),
                                Regexp(r'^[a-zA-Z0-9]+$',
                                       message='Недопустимые символы в ссылке')
                            ])
    submit = SubmitField('Создать короткую ссылку')
