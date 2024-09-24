# models Две модели, где города будут связаны с конкретной страной с помощью внешнего ключа.
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

# forms Форма будет включать два выпадающих списка: один для стран, другой для городов, которые будут обновляться через AJAX на основе выбранной страны.
from django import forms
from .models import Country, City

class LocationForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label="Country")
    city = forms.ModelChoiceField(queryset=City.objects.none(), label="City")

# views Добавляем в views функцию для AJAX-запросов, которая будет возвращать список городов, относящихся к выбранной стране.
from django.http import JsonResponse
from .models import City

def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

# urls Нужно добавить URL для AJAX-запроса.
from django.urls import path
from . import views

urlpatterns = [
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]

# Шаблон и jquery скрипт (его можно вынести в отдельный файл
<form method="POST">
    {% csrf_token %}
    {{ form.country }}
    {{ form.city }}
    <button type="submit">Submit</button>
</form>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script type="text/javascript">
    $(document).ready(function () {
        $("#id_country").change(function () {
            var url = "{% url 'ajax_load_cities' %}";  // Получаем URL для запроса
            var countryId = $(this).val();  // Получаем выбранную страну

            $.ajax({
                url: url,
                data: {
                    'country_id': countryId
                },
                success: function (data) {
                    $("#id_city").html('');  // Очищаем предыдущие значения
                    $.each(data, function (key, value) {
                        $("#id_city").append('<option value="' + value.id + '">' + value.name + '</option>');
                    });
                }
            });
        });
    });
</script>

