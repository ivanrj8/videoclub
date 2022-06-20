from django import forms
#from ofertasTrabajo.models import Usuario,Categoria,Oferta


class FrmLogin(forms.Form):  # login
    usuarioLogin = forms.CharField(max_length=16, widget=forms.TextInput(
        {'class': 'form-control', 'placeholder': "Usuario"}))
    passwordLogin = forms.CharField(max_length=16, widget=forms.PasswordInput({
                                    'class': 'form-control', 'placeholder': "Password"}))


class FrmAddUser(forms.Form):  # add
    usuario = forms.CharField(max_length=16, widget=forms.TextInput(
        {'class': 'form-control', 'placeholder': "Usuario"}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(
        {'class': 'form-control', 'placeholder': "Password"}))
