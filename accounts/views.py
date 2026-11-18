from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def login_view(request):
    return render(request, 'accounts/login.html')

def signup_view(request):
    User = get_user_model()

    errors = []
    success = None

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Check full name
        if not full_name:
            errors.append("Please enter your full name.")

        # Check whether email already exists
        if User.objects.filter(email__iexact=email).exists():
            errors.append("This email is already registered.")

        # Check passwords
        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Validate password strength
        user = User(email=email, first_name=full_name)

        try:
            validate_password(password, user=user)
        except ValidationError as e:
            errors.extend(e.messages)

        # Create account if there are no errors
        if not errors:
            user.set_password(password)
            user.is_active = False
            user.is_email_verified = False
            user.is_approved = False
            user.save()

            success = "Your account has been created! Email verification will be available soon."

    return render(request, "accounts/signup.html", {
        "errors": errors,
        "success": success
    })