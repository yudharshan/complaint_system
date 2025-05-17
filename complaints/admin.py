from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Complaint

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'id_number', 'email', 'is_student', 'is_staff_member')
    list_filter = ('is_student', 'is_staff_member')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('id_number', 'is_student', 'is_staff_member')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('id_number', 'is_student', 'is_staff_member')}),
    )

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_complaint_type_display', 'get_status_display', 'severity', 'created_at')
    list_filter = ('complaint_type', 'status')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'resolved_at')
    
    fieldsets = (
        (None, {'fields': ('user', 'complaint_type', 'description', 'severity', 'status')}),
        ('Hostel Details', {'fields': ('room_number',), 'classes': ('collapse',)}),
        ('Faculty Details', {'fields': ('department', 'faculty_name'), 'classes': ('collapse',)}),
        ('Library Details', {'fields': ('library_issue_type', 'book_name'), 'classes': ('collapse',)}),
        ('Dates', {'fields': ('created_at', 'resolved_at'), 'classes': ('collapse',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Complaint, ComplaintAdmin)