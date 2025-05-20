from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Book

# Форма регистрации пользователя с выбором роли
class RegistrationForm(UserCreationForm):
    user_role = forms.ChoiceField(choices=[('user', 'Обычный пользователь'), ('admin', 'Администратор')])

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'password1', 'password2', 'user_role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"]
        user.user_role = self.cleaned_data["user_role"]
        if commit:
            user.save()
        return user

# Форма входа
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Форма книги
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price']

# Форма регистрации пользователя (дополнительная версия с выбором роли)
class CustomUserRegistrationForm(UserCreationForm):
    user_role = forms.ChoiceField(choices=[('user', 'Обычный пользователь'), ('admin', 'Администратор')])

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'user_role')
