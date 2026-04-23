from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import TemplateView
from app.form import RegisterForm, EmailLoginForm
from app.models import User
from app.utils import generate_code, send_register_email
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailBackendForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Emailingizni yozing'
    }))

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")  # <--- Endi bu xatosiz ishlaydi

    def form_valid(self, form):
        user = form.save()



        user = form.save()


        code = generate_code()


        self.request.session["verify_user_id"] = user.id
        self.request.session["verify_code"] = str(code)

        # 4. Email yuboramiz
        if user.email:
            send_register_email(
                to_email=user.email,
                code=code
            )

     # ... qolgan kodlaringiz (email yuborish va h.k.)

        return redirect("login")



    def form_invalid(self, form):
        # Xatolarni ko'rish uchun (terminalda)
        print("❌ ERRORS:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class VerifyEmailView(TemplateView):
    template_name = "confirm-password.html"

    def post(self, request, *args, **kwargs):
        if request.POST.get("code") != request.session.get("verify_code"):
            return redirect("verify-email")

        user = User.objects.get(id=request.session["verify_user_id"])
        user.is_active = True
        user.save()

        request.session.pop("verify_code", None)
        request.session.pop("verify_user_id", None)
        return redirect("login")


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


class UserLoginView(LoginView):
    template_name = 'login.html'  # Login sahifangiz nomi
    authentication_form = EmailBackendForm

    # redirect_authenticated_user = True  # Agar foydalanuvchi allaqachon login bo'lgan bo'lsa, avtomatik indexga o'tkazadi

    def get_success_url(self):
        """Muvaffaqiyatli kirishdan keyin index sahifasiga o'tkazish"""
        return reverse_lazy('index')

    def form_invalid(self, form):
        """Agar login yoki parol xato bo'lsa, foydalanuvchiga xabar ko'rsatish"""
        messages.error(self.request, "Login yoki parol noto'g'ri. Iltimos, qaytadan urinib ko'ring.")
        return super().form_invalid(form)




class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

    def post(self, request):
        logout(request)
        return redirect("login")

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from app.models import User
from app.utils import generate_code, send_register_email


class ForgotPasswordView(TemplateView):
    template_name = 'forgot-password.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, self.template_name,
                          {'error': 'Bunday foydalanuvchi topilmadi'})
        code = generate_code()
        request.session['reset_code'] = code
        request.session['reset_user_id'] = user.id
        send_register_email(user.email, code)
        return redirect('reset-password')


class ResetPasswordView(TemplateView):
    template_name = 'reset-password.html'

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if code != str(request.session.get('reset_code')):
            return render(request, self.template_name, {'error': 'Kod noto‘g‘ri'})
        if password != confirm_password:
            return render(request, self.template_name, {'error': 'Parollar bir xil emas'})
        user = User.objects.filter(id=request.session.get('reset_user_id')).first()
        if not user:
            return redirect('forgot-password')
        user.set_password(password)
        user.save()
        request.session.pop('reset_code', None)
        request.session.pop('reset_user_id', None)
        return redirect('login')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, FormView
from app.form import ContactForm
from app.models import Portfolio, Product


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'

    model = Product
    paginate_by = 3
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_range"] = range(1, 6)
        context["top_products"] = Product.objects.order_by('-review')[:4]
        return context


class BizHaqimizdaView(LoginRequiredMixin,TemplateView):
    template_name = 'biz-haqimizda.html'


class ConfirmPasswordView(LoginRequiredMixin,TemplateView):
    template_name = 'biz-haqimizda.html'


class BlogListView(LoginRequiredMixin,ListView):
    model = Portfolio
    paginate_by = 3
    template_name = 'blog.html'
    context_object_name = 'portfolio'


class BlogDetailView(DetailView):
    template_name = 'blog-detail.html'

    model = Portfolio
    context_object_name = 'portfolio'


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class SavatchaView(LoginRequiredMixin,TemplateView):
    template_name = 'savatcha.html'


class AloqaView(LoginRequiredMixin,FormView):
    template_name = 'aloqa.html'
    form_class = ContactForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView

from app.models import Product


class MahsulotListView(LoginRequiredMixin, ListView):
    template_name = 'mahsulotlar.html'
    model = Product
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q')

        sort = self.request.GET.get('sort')
        if sort == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'rating_desc':
            queryset = queryset.order_by('-review')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q))


        return queryset

class MahsulotDetailView(DetailView):
    template_name = 'mahsulot-detail.html'
    model = Product
    context_object_name = 'product'


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


