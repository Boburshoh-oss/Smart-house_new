from django import forms
from django.contrib import admin

from .models import (Channel, Condition, Device, Home, Product, Sensor,
                     Sensor_cache, SmartCondition)

# # Register your models here.
# admin.site.register(SmartCondition)
# admin.site.register(SensorState)
# admin.site.register(Condition)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)



    
class ChannelItemInline(admin.TabularInline):
    model = Channel
    extra = 0

class SensorItemInline(admin.TabularInline):
    model = Sensor
    extra = 0


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = True
        self.fields['home'].required = True
        self.fields['name'].required = True

    class Meta:
        model = Device
        fields = '__all__'

class DeviceAdmin(admin.ModelAdmin):
    form = PostForm
    inlines = [ChannelItemInline,SensorItemInline]
    list_display = ("owner","name", "product", "home","created_at","updated_at")
    list_filter = ("name", "product", "home","owner")
    search_fields = ("name", "product", "home")
    ordering = ("name", "product", "home")
    class Meta:
        model = Device
admin.site.register(Device,DeviceAdmin)

admin.site.register(Sensor)
admin.site.register(Product)
admin.site.register(Home)
admin.site.register(Sensor_cache)
admin.site.register(SmartCondition)
admin.site.register(Condition)