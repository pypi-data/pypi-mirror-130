{% for api in service.apis %}
Future<{{ api.response_type_pascal_case }}> {{ api.name_camel_case }}({{ api.request_type_pascal_case }} request);
{{- '\n' if not loop.last }}
{% endfor %}