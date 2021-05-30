from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """
    # email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email']