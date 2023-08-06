from jinja2 import Template

class TerraformTemplate(Template):
    pass



standard_resource = Template(
'''
resource "{{ object_name }}" {
{% for option, value in object_options.items() -%}
{{ option | indent }} = {{ value[1:] if value.startswith('_') else (value | quote) }}
{% endfor -%}
}
'''
)
