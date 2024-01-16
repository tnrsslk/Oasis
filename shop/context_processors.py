# Импортируем модель Category из текущего (текущего приложения) пакета (.)
from .models import Category

# Определяем функцию category_list, которая будет использоваться в контексте шаблона
def category_list(request):
    return {
        'categories': Category.objects.all(),
    }
