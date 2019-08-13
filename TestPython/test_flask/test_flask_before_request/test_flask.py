
def set_limited_routes_details():
    for rule in app.url_map.iter_rules():
        if rule.endpoint.lstrip('api.') in limited_routes:
            regex = re.compile(rule._regex.pattern.replace('\\|', '', 1))
            limited_routes_details[rule.endpoint] = {
                'regex': regex,
                'arguments': list(rule.arguments),
                'partial_route': rule.rule.replace('/api/v1', "", 1),
            }