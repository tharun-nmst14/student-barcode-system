import os
import barcode
from barcode.writer import ImageWriter
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})


@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        roll = request.POST['roll']
        email = request.POST['email']
        department = request.POST['department']

        if Student.objects.filter(roll_number=roll).exists():
            messages.error(request, f"Roll number {roll} already exists!")
            return render(request, 'core/add_student.html')

        # Create student
        student = Student(name=name, roll_number=roll, email=email, department=department)
        student.save()

        # Generate barcode
        from barcode import Code128
        from barcode.writer import ImageWriter

        barcode_class = Code128(student.roll_number, writer=ImageWriter())
        barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        os.makedirs(barcode_dir, exist_ok=True)

        file_path = os.path.join(barcode_dir, f"{student.roll_number}")
        barcode_class.save(file_path)

        student.barcode_image = f"barcodes/{student.roll_number}.png"
        student.save()

        messages.success(request, "Student added successfully!")
        return redirect('student_list')

    return render(request, 'core/add_student.html')

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.roll_number = request.POST['roll']
        student.email = request.POST['email']
        student.department = request.POST['department']
        student.year = request.POST.get('year')
        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect('student_list')

    return render(request, 'core/edit_student.html', {'student': student})


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('student_list')
    return render(request, 'core/delete_student.html', {'student': student})


@login_required
def student_detail(request, roll_number):
    try:
        student = Student.objects.get(roll_number=roll_number)
        return JsonResponse({
            "name": student.name,
            "roll_number": student.roll_number,
            "email": student.email,
            "department": student.department
        })
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    
@login_required
def student_profile(request, roll_number):
    student = get_object_or_404(Student, roll_number=roll_number)
    return render(request, 'core/student_profile.html', {'student': student})
