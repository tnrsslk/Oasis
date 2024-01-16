# Импортируем модуль forms из библиотеки Django
from django import forms
# Импортируем модель ReviewRating из текущего (текущей) директории
from .models import ReviewRating

# Определяем форму для ввода отзыва и рейтинга
class ReviewForm(forms.ModelForm):
    class Meta:
        # Указываем, что моделью для формы будет ReviewRating
        model = ReviewRating
        # Указываем, какие поля из модели будут использоваться в форме
        fields = ['review', 'rating']
