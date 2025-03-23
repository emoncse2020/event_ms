from django import forms
from .models import Event, Participant, Category


class StyledFormMixin:
    """ Mixing to apply style to form field"""

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-cyan-500 focus:ring-cyan-600"

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': "",
                    'type':'time',
                })
            else:
               
                field.widget.attrs.update({
                    'class': self.default_classes
                })





class EventModelForm(StyledFormMixin,forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'date','time','location', 'category']

        widgets= {
            'date': forms.SelectDateWidget(),
            'time':forms.TimeInput()
        }


class ParticipantModelForm(StyledFormMixin,forms.ModelForm):
    
    class Meta:
        model = Participant
        fields = ['name', 'email']

       



