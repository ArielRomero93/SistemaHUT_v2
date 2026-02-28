from django import forms
from .models import FormularioInscripcionHUT, Pais, ProvinciaEstado, CursoHUT

INPUT_CLASS = (
    'form-input'
)

SELECT_CLASS = (
    'form-input'
)


class InscripcionForm(forms.ModelForm):
    # Extra field for WhatsApp number (without country code)
    whatsapp_codigo = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'whatsapp_codigo'}),
    )
    whatsapp_numero = forms.CharField(
        max_length=15,
        label='WhatsApp',
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Tu número sin el 0',
            'type': 'tel',
            'id': 'whatsapp_numero',
            'inputmode': 'tel',
        }),
    )

    class Meta:
        model = FormularioInscripcionHUT
        fields = [
            'nombre', 'apellido', 'edad', 'pais', 'provincia',
            'ciudad', 'telefono', 'congregacion', 'pastor',
            'email', 'estadoCivil'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: María',
            }),
            'apellido': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: García',
            }),
            'edad': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: 35',
                'min': 13,
                'max': 99,
                'inputmode': 'numeric',
            }),
            'pais': forms.Select(attrs={
                'class': SELECT_CLASS,
                'id': 'id_pais',
            }),
            'provincia': forms.Select(attrs={
                'class': SELECT_CLASS,
                'id': 'id_provincia',
            }),
            'ciudad': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: Córdoba',
            }),
            'telefono': forms.HiddenInput(attrs={
                'id': 'id_telefono',
            }),
            'congregacion': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nombre de tu iglesia',
            }),
            'pastor': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nombre de tu pastor/a',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'correo@ejemplo.com',
                'inputmode': 'email',
            }),
            'estadoCivil': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'edad': 'Edad',
            'pais': 'País',
            'provincia': 'Provincia / Estado',
            'ciudad': 'Ciudad',
            'telefono': 'WhatsApp',
            'congregacion': 'Congregación / Iglesia',
            'pastor': 'Pastor/a',
            'email': 'Correo Electrónico',
            'estadoCivil': 'Estado Civil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].queryset = Pais.objects.all().order_by('paisNombre')
        self.fields['provincia'].queryset = ProvinciaEstado.objects.none()
        self.fields['telefono'].required = False

        # Guardar el curso activo para usar en validaciones
        self.curso_activo = CursoHUT.objects.filter(activo=True).first()

        if 'pais' in self.data:
            try:
                pais_id = int(self.data.get('pais'))
                self.fields['provincia'].queryset = ProvinciaEstado.objects.filter(
                    idPais_id=pais_id
                ).order_by('provinciaNombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['provincia'].queryset = (
                self.instance.pais.provinciaestado_set.order_by('provinciaNombre')
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.curso_activo:
            if FormularioInscripcionHUT.objects.filter(
                email__iexact=email, curso=self.curso_activo
            ).exists():
                raise forms.ValidationError('Ya existe una inscripción con este correo electrónico para este curso.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        codigo = cleaned_data.get('whatsapp_codigo', '')
        numero = cleaned_data.get('whatsapp_numero', '')
        if numero:
            telefono_completo = f"+{codigo}{numero}" if codigo else numero
            cleaned_data['telefono'] = telefono_completo
            # Validar teléfono duplicado solo dentro del curso activo
            if self.curso_activo and FormularioInscripcionHUT.objects.filter(
                telefono=telefono_completo, curso=self.curso_activo
            ).exists():
                self.add_error('whatsapp_numero', 'Ya existe una inscripción con este número de teléfono para este curso.')
        else:
            self.add_error('whatsapp_numero', 'Este campo es obligatorio.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.curso_id and self.curso_activo:
            instance.curso = self.curso_activo
        if commit:
            instance.save()
        return instance
