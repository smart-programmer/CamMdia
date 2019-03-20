from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, length, Email
from wtforms_components import SelectField

subFilters = (
    ("logos", "شعارات"),
    ("brochures", "بروشورات"),
    ("banner", "بنرات"),
    ("visualIdentity", "هوية بصرية"),
    ("folders", "فولدرات"),
)


class MessageForm(FlaskForm):
    full_name = wtforms.StringField(
        "الاسم ", validators=[length(min=3, max=255)])
    email = wtforms.StringField("البريد الإلكتروني", validators=[
                                Email(), DataRequired(), length(max=255)])
    subject = wtforms.StringField("عنوان الرسالة", validators=[
                                  length(min=3, max=255)])
    content = wtforms.TextAreaField("نص الرسالة ", validators=[
                                    DataRequired(), length(max=1000)])
    submit = wtforms.SubmitField("أرسل")


class LoginForm(FlaskForm):
    email = wtforms.StringField("البريد الإلكتروني")
    password = wtforms.StringField("الرقم السري")
    submit = wtforms.SubmitField("تسجيل الدخول")


class UploadImage(FlaskForm):
    title = wtforms.StringField("عنوان الصورة ", validators=[
                                DataRequired(), length(min=3, max=255)])
    description = wtforms.StringField(" وصف الصورة ", validators=[
        DataRequired(), length(min=3, max=255)])
    url = wtforms.StringField("  رابط للصورة ", validators=[
        length(min=3, max=255)])
    filters = SelectField("التصنيف", choices=subFilters,
                          validators=[DataRequired()])
    submit = wtforms.SubmitField("أرفع")


class UploadTestimonial(FlaskForm):
    name = wtforms.StringField(" اسم العمييل ", validators=[
        DataRequired(), length(min=3, max=255)])
    work = wtforms.StringField("  طبيعة عمله ", validators=[
        DataRequired(), length(min=3, max=255)])
    description = wtforms.StringField("   ماقله العمييل ", validators=[
        length(min=3, max=500)])

    submit = wtforms.SubmitField("أرفع")


class ReplyForm(FlaskForm):
    subject = wtforms.StringField("عنون الرسالة", validators=[
        length(max=255)])
    email = wtforms.StringField("البريد الإلكتروني", validators=[
        Email(), DataRequired(), length(max=255)])
    message = wtforms.TextAreaField("نص الرسالة ", validators=[
                                    DataRequired(), length(max=1000)])
    submit = wtforms.SubmitField("أرسل")
