from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Complaint

class CustomUserCreationForm(UserCreationForm):
    id_number = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'id_number', 'password1', 'password2')

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'description', 'severity', 'room_number', 
                 'department', 'faculty_name', 'library_issue_type', 'book_name']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show/hide fields based on complaint type
        if 'complaint_type' in self.data:
            complaint_type = self.data['complaint_type']
            if complaint_type == 'hostel':
                self.fields['room_number'].required = True
            elif complaint_type == 'faculty':
                self.fields['department'].required = True
                self.fields['faculty_name'].required = True
            elif complaint_type == 'library':
                self.fields['library_issue_type'].required = True
                if 'library_issue_type' in self.data and self.data['library_issue_type'] == 'book_not_found':
                    self.fields['book_name'].required = True