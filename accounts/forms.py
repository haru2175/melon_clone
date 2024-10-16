from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import User

# Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("username", "password1", "password2")
    helper.add_input(Submit("submit", "회원가입", css_class="w-100"))


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("username", "password")
    helper.add_input(Submit("submit", "로그인", css_class="w-100"))


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["avatar"]
#
#     helper = FormHelper()
#     helper.attrs = {"novalidate": True}
#     helper.layout = Layout("avatar")
#     helper.add_input(Submit(name="submit", value="저장", css_class="w-100"))
