from django.forms import widgets


class ImageInput(widgets.FileInput):
    template_name = 'widgets/image_input.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'accept': 'image/*', 'class': 'sr-only'})


class CheckboxInput(widgets.CheckboxInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update(
            {
                'class': (
                    'h-4 w-4 rounded border-gray-300 '
                    'text-indigo-600 focus:ring-indigo-600'
                )
            }
        )
