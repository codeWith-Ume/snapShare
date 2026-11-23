from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def login_view(request):

    errors = []

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            if not user.is_approved or not user.is_active:
                errors.append("Your account is waiting for admin approval.")
            else:
                login(request, user)
                request.session["login_success"] = "Login successful! Welcome back."
                return redirect("home")

        else:
            User = get_user_model()
            pending_user = User.objects.filter(email__iexact=email).first()

            if pending_user and pending_user.check_password(password):
                if not pending_user.is_approved or not pending_user.is_active:
                    errors.append("Your account is waiting for admin approval.")
                else:
                    errors.append("Invalid email or password.")
            else:
                errors.append("Invalid email or password.")

    return render(request, "accounts/login.html", {
        "errors": errors
    })



def signup_view(request):
    User = get_user_model()

    errors = []
    success = None

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not full_name:
            errors.append("Please enter your full name.")

        if not email:
            errors.append("Please enter your email.")

        if User.objects.filter(email__iexact=email).exists():
            errors.append("This email is already registered.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        user = User(email=email, first_name=full_name)

        try:
            validate_password(password, user=user)
        except ValidationError as e:
            errors.extend(e.messages)

        if not errors:
            user.set_password(password)
            user.is_email_verified = True

            if email.lower().endswith("@navgurukul.org"):
                user.is_active = True
                user.is_approved = True
                user.save()

                login(request, user)
                request.session["login_success"] = "Account created successfully! Welcome."
                return redirect("home")

            else:
                user.is_active = False
                user.is_approved = False
                user.save()

                success = "Your signup request has been submitted. Please wait for admin approval."

    return render(request, "accounts/signup.html", {
        "errors": errors,
        "success": success
    })


def logout_view(request):
    logout(request)
    return redirect("home")