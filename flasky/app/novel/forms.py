from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class SearchForm(FlaskForm):
    search = StringField('请输入要搜索的内容:', validators=[Required(), Length(1, 64)])
    submit = SubmitField('提交')
