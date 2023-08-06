from string import Template

from public import public


@public
class TXT(Template):
    def __init__(self, template_str, locals=None, globals=None):
        if globals is None:
            globals = {}

        if locals is None:
            locals = {}

        self.vars = locals | globals
        self.substitute(self.vars)
        super().__init__(template_str)

    def localize(self, lang):
        return self.substitute(self.vars)
