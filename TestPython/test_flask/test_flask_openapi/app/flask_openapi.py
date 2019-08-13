from openapi_core.wrappers.flask import FlaskOpenAPIRequest


class FlaskOpenAPIRequestWrapper(FlaskOpenAPIRequest):
    @property
    def path_pattern(self):
        if self.request.url_rule is None:
            return self.path
        rule = self.request.url_rule.rule.replace('<', '{').replace('>', '}').replace('int:', '').replace('string:', '')
        print(rule, self.method)
        return rule

    @property
    def parameters(self):
        return {
            'path': self.request.view_args,
            'query': self.request.args,
            'header': self.request.headers,
            'cookie': self.request.cookies,
        }
