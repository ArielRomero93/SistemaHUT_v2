from django import forms
from .models import FormularioInscripcionHUT, Pais, ProvinciaEstado, CursoHUT, GruposMoodle, Voluntario

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


class GruposMoodleForm(forms.ModelForm):
    class Meta:
        model = GruposMoodle
        fields = ['nombre', 'curso', 'horario', 'dia', 'tutor', 'url_whatsapp', 'capacidad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: Grupo 1',
            }),
            'curso': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
            'horario': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: 19:00 a 21:00 hs',
            }),
            'dia': forms.Select(attrs={
                'class': SELECT_CLASS,
            }),
            'tutor': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: Juan Pérez',
            }),
            'url_whatsapp': forms.URLInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Ej: https://chat.whatsapp.com/...',
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': '1',
            }),
        }

class InscriptoLoginForm(forms.Form):
    codigo_acceso = forms.CharField(
        label='Código Único de Acceso',
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Ej: HUT-8XJ92',
        })
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'correo@ejemplo.com',
        })
    )

class SeleccionGrupoForm(forms.ModelForm):
    class Meta:
        model = FormularioInscripcionHUT
        fields = ['grupo']
        widgets = {
            'grupo': forms.Select(attrs={
                'class': SELECT_CLASS,
            })
        }
        labels = {
            'grupo': 'Selecciona tu Grupo Moodle'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo'].required = True
        self.fields['grupo'].error_messages = {'required': 'Debes seleccionar un grupo para continuar.'}
        if self.instance and self.instance.pk:
            # Usar siempre el curso activo globalmente para mostrar los grupos disponibles
            curso_activo = CursoHUT.objects.filter(activo=True).first()
            if not curso_activo:
                curso_activo = self.instance.curso

            # Filter groups that belong to the active course and have available capacity
            from django.db.models import F, Q
            
            if self.instance.grupo_id:
                grupos_disponibles = GruposMoodle.objects.filter(
                    Q(curso=curso_activo, participantes__lt=F('capacidad')) |
                    Q(id=self.instance.grupo_id)
                )
            else:
                grupos_disponibles = GruposMoodle.objects.filter(
                    curso=curso_activo,
                    participantes__lt=F('capacidad')
                )
            
            self.fields['grupo'].queryset = grupos_disponibles
            self.fields['grupo'].empty_label = "Elige un grupo disponible..."
            self.fields['grupo'].label_from_instance = lambda obj: f"{obj.nombre} ({obj.dia} {obj.horario}) - {obj.capacidad - obj.participantes} vacantes"

    def clean_grupo(self):
        grupo = self.cleaned_data.get('grupo')
        if not grupo:
            raise forms.ValidationError("Debes seleccionar un grupo para continuar.")
            
        grupo.refresh_from_db()
        if grupo.participantes >= grupo.capacidad:
            raise forms.ValidationError("Este grupo ya está lleno. Por favor, elige otro.")
        return grupo

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = '__all__'
        widgets = {
            'areas_interes': forms.CheckboxSelectMultiple(),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

