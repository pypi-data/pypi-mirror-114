from platformer.templates.base_terraform import standard_resource

class TerraformCoder:
    def __init__(self, pf_definition):
        self.pf_definition = pf_definition
        self.modules = [module for module in pf_definition["modules"]]

    def render(self, resource):
        return standard_resource.render(
            object_name = resource["name"],
            object_options = resource["options"]
        )

    def filter_module_type(self, query):
        return list(filter(
            lambda mod: mod["type"] == query, self.modules
        ))

    def get_rendered_list(self):
        return [
            self.render(module)
            for module in self.filter_module_type("raw_resource")
        ]

    def print_code(self):
        return '\n'.join(self.get_rendered_list())


