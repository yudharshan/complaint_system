from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone  # Added import
from .forms import CustomUserCreationForm, ComplaintForm
from .models import Complaint

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Safer access
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', 
                        {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('dashboard')
        # If form is invalid, it will be re-rendered with errors
    else:
        form = ComplaintForm()
    
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/dashboard.html', 
                {'form': form, 'complaints': complaints})

@staff_member_required
def admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filtering
    complaint_type = request.GET.get('type')
    if complaint_type:
        complaints = complaints.filter(complaint_type=complaint_type)
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'severity':
        complaints = complaints.order_by('-severity')
    
    return render(request, 'complaints/admin_dashboard.html', 
                {'complaints': complaints})

@staff_member_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)  # Safer object retrieval
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:  # Check if status was provided
            complaint.status = status
            if status == 'resolved':
                complaint.resolved_at = timezone.now()
            complaint.save()
            return redirect('admin_dashboard')
    return render(request, 'complaints/update_status.html', 
                {'complaint': complaint})