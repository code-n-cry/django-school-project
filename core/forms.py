from django import forms


class BaseTailwindForm(forms.Form):
    error_class = 'border-red-700'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if not field.field.widget.attrs.get('class'):
                field.field.widget.attrs.update(
                    {
                        'class': (
                            'block w-full rounded-md bg-white '
                            'border-0 py-1.5 pl-7 pr-20 '
                            'text-gray-900 ring-1 '
                            'ring-inset ring-gray-300 '
                            'placeholder:text-gray-400 '
                            'focus:ring-2 focus:ring-inset '
                            'focus:ring-indigo-600 '
                            'sm:text-sm sm:leading-6'
                        )
                    }
                )


class BaseTailwindModelForm(BaseTailwindForm, forms.ModelForm):
    ...
