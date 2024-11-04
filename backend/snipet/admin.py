from django.contrib import admin
from snipet.models import *
from store.models import *
from django.utils.html import format_html
# Register your models here.



class shipformedesAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("China","USA", "updated_at","created_at",)
    
    
admin.site.register(shipformedes, shipformedesAdmin)
class shipformemesssagesAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("China","USA", "updated_at","created_at",)
    
    
admin.site.register(shipformemesssages, shipformemesssagesAdmin)


class shipformechargeAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("China_charge","China_days","USA_charge","USA_days", "updated_at","created_at",)


admin.site.register(shipformecharge, shipformechargeAdmin)


class shipformenoteAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("Description", "updated_at","created_at",)



admin.site.register(shipformenote, shipformenoteAdmin)

class payformenoteAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("Description", "updated_at","created_at",)



admin.site.register(payformenote, payformenoteAdmin)

class Home_BanneerAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("images","name", "updated_at","created_at",)
    def images(self, obj):
        return format_html(f'<img style="overflow: hidden; width: 4rem; height: 4rem; border-radius: 0.25rem; border-width: 1px; border-color: #E5E7EB;" src="/{obj.image}" alt="">')


admin.site.register(Home_Banneer, Home_BanneerAdmin)



class reqsnoteAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("Description", "updated_at","created_at",)
   

admin.site.register(reqsnote, reqsnoteAdmin)


class Home_FaqAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("question","answer", "updated_at","created_at",)


admin.site.register(Home_Faq, Home_FaqAdmin)

class Faq_pageAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("question","answer", "updated_at","created_at",)


admin.site.register(Faq_page, Faq_pageAdmin)


class terms_condition_pageAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("question","answer", "updated_at","created_at",)


admin.site.register(terms_condition_page, terms_condition_pageAdmin)



class forbidenitempagen_pageAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("Item_Name", "updated_at","created_at",)


admin.site.register(forbidenitempagen_page, forbidenitempagen_pageAdmin)

class Shipping_refund_Pollicy_pageAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("question","answer", "updated_at","created_at",)


admin.site.register(Shipping_refund_Pollicy_page, Shipping_refund_Pollicy_pageAdmin)

class Privacy_Policy_pageeAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("question","answer", "updated_at","created_at",)


admin.site.register(Privacy_Policy_page, Privacy_Policy_pageeAdmin)

class Home_CatagorysAdmin(admin.ModelAdmin):
    """ticket admin."""

    list_display = ("catagory","name","home_page", )

admin.site.register(Home_Catagorys,Home_CatagorysAdmin)

admin.site.register(Catagorys)



@admin.register(D_Rate)
class D_RateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in D_Rate._meta.fields]


@admin.register(Site_Identity)
class Site_IdentityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Site_Identity._meta.fields]

@admin.register(Home_top600px_Banneer)
class Home_top600px_BanneerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_top600px_Banneer._meta.fields]

@admin.register(Home_middel502x202px_Banneer)
class Home_middel502x202px_BanneerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_middel502x202px_Banneer._meta.fields]

@admin.register(Home_middel680x180px_Banneer)
class Home_middel680x180px_BanneerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_middel680x180px_Banneer._meta.fields]

@admin.register(Home_bottom_sites_Banneer)
class Home_bottom_sites_BanneerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_bottom_sites_Banneer._meta.fields]

@admin.register(Home_sliding_selling_text_Banneer)
class Home_sliding_selling_text_BanneerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_sliding_selling_text_Banneer._meta.fields]


@admin.register(Home_4data_breadcum)
class Home_4data_breadcumAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Home_4data_breadcum._meta.fields]
    

class SubCatagorysListInline(admin.TabularInline):  # Use admin.StackedInline for a different layout
    model = SubCatagorysList
    
@admin.register(CatagorysList)
class CatagorysListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CatagorysList._meta.fields]
    inlines = [SubCatagorysListInline]

@admin.register(SubCatagorysList)
class SubCatagorysListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SubCatagorysList._meta.fields]

@admin.register(FooterLinks)
class FooterLinksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FooterLinks._meta.fields]

@admin.register(FooterWidget)
class FooterWidgetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FooterWidget._meta.fields]

@admin.register(FooterPaymentSuportImage)
class FooterPaymentSuportImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FooterPaymentSuportImage._meta.fields]

@admin.register(aboustuspage)
class aboustuspageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in aboustuspage._meta.fields]

@admin.register(Payment_numbers)
class Payment_numbersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment_numbers._meta.fields]

@admin.register(Google_Tag_Manager)
class Google_Tag_ManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Google_Tag_Manager._meta.fields]