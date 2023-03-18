from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonMixin
from products.models import Basket, Product, User
# from users.models import User
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')


class UserRegistrationView(SuccessMessageMixin, CommonMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = '''Ваш аккаунт успешно зарегестрирован! 
        Для подтверждения электронной почты мы выслали вам письмо'''
    success_url = reverse_lazy('users:login')
    title = 'Store - Регистрация'

    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        user = queryset.get(pk=self.request.user.id)
        return user


class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_message = 'Данные успешно обновлены!'
    template_name = 'users/profile.html'
    title = 'Store - Профиль'
    # success_url = reverse_lazy('users:profile')

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs) :
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


class EmailVerificationView(CommonMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)

        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verirified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))           
#     else:
#         form = UserLoginForm()
#     context = {'form':form}
#     return render(request, 'users\login.html', context)

# def logout(request):
#     auth.logout(request)  
#     return HttpResponseRedirect(reverse('index'))

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)   
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Данные успешно обновлены!')
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)

#     context = {
#         'title':'Store - Профиль', 
#         'form':form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Ваш аккаунт успешно зарегестрирован!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'form':form}
#     return render(request, 'users/register.html', context)