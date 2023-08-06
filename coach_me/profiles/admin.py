from django.contrib import admin
from coach_me.profiles.models import BookingUserProfile, Company


#
#
# # Register your models here.
#
@admin.register(BookingUserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'company', 'newsletter_subscription', 'is_lector')

    list_filter = ('newsletter_subscription', 'is_lector', 'company')

    search_fields = ('first_name', 'last_name', 'company')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'picture', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('private_email', 'phone', 'company')
        }),
        ('Consent and Subscription', {
            'fields': ('consent_terms', 'newsletter_subscription')
        }),
        ('Lector Information', {
            'fields': ('is_lector',)
        }),
    )

    date_hierarchy = 'date_of_birth'

    ordering = ['last_name', 'first_name']

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    show_full_result_count = True

    # Property for full name
    def full_name(self, obj):
        return obj.full_name

    full_name.admin_order_field = 'last_name'  # Sort by last name


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'short_company_name',
        'legal_company_name',
        'contact_person_names',
        'contact_person_email',
        'contact_person_phone',
    )
    list_filter = (
        'contract_start_date',
        'contract_end_date',
    )
    search_fields = (
        'short_company_name',
        'legal_company_name',
        'contact_person_names',
        'contact_person_email',
        'contact_person_phone',
    )

    fieldsets = (
        ('Company Information', {
            'fields': ('short_company_name', 'legal_company_name', 'company_register_number', 'slug')
        }),
        ('Contact Person Information', {
            'fields': ('contact_person_names', 'contact_person_role', 'contact_person_email', 'contact_person_phone')
        }),
        ('Contract Information', {
            'fields': ('contract_start_date', 'contract_end_date')
        }),
    )

    date_hierarchy = 'contract_start_date'

    ordering = ['-contract_start_date']

    list_select_related = True

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    actions_on_bottom = True

    actions_on_top = False

    show_full_result_count = True

    list_editable = (
        'short_company_name',
        'contact_person_names',
        'contact_person_email',
        'contact_person_phone',
    )
