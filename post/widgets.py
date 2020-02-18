from django import forms


class starWidget(forms.TextInput):
    input_type = 'rating'
    template_name = "widgets/star_rate.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.update({
            'min': 0,
            'max': 5,
            'step': 1,
        })
        return attrs
