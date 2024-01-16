from django import forms
from .models import Account, UserProfile

# Форма для регистрации пользователя
class RegisterationFrom(forms.ModelForm):
    # Поля для ввода пароля и его подтверждения
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        # Определение полей, которые должны быть включены в форму
        fields = ['first_name', 'last_name', 'Phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterationFrom, self).__init__(*args, **kwargs)
        # Установка атрибутов класса для виджетов полей ввода
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input100'

    def clean(self):
        cleaned_data = super(RegisterationFrom, self).clean()
        # Проверка, совпадают ли пароль и его подтверждение
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('repeat_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

# Форма для редактирования основных данных пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'Phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Установка класса для виджетов полей ввода
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# Форма для редактирования профиля пользователя
class UserProfileForm(forms.ModelForm):
    # Поле для загрузки изображения профиля
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")},
                                       widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Установка класса для виджетов полей ввода
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
