{% for api in service.apis %}
{{ '' }}
@override
Future<{{ api.response_type_pascal_case }}> {{ api.name_camel_case }}({{ api.request_type_pascal_case }} request) async {
  final service = await _{{ service.name_camel_case }}ApiService;
  return await service.{{ api.name_camel_case }}(
    {% for header in api.dynamic_headers %}
    request.headers.{{ header.title_camel_case}},
    {% endfor %}
    {% for path_camel_case in api.path_from_endpoint.values() %}
    request.paths.{{ path_camel_case }},
    {% endfor %}
    {% if api.queries|length > 0 %}
    request.queries.toMap(),
    {% endif %}
    {% if api.body|length > 0 %}
    request.body.toMap(),
    {% endif %}
    {% for field in api.fields %}
    request.fields.{{ field.title_camel_case }},
    {% endfor %}
    {% for part in api.parts %}
    {% if part.is_file_type %}
    {% if part.is_list_type %}
    request.parts.{{ part.title_camel_case }}.map((filePath) => File(filePath)).toList(),
    {% else %}
    File(request.parts.{{ part.title_camel_case }}),
    {% endif %}
    {% else %}
    request.parts.{{ part.title_camel_case }},
    {% endif %}
    {% endfor %}
  );
}
{% endfor %}

Future<{{ service.name_pascal_case }}ApiService> get _{{ service.name_camel_case }}ApiService async {
  final dio = await _createDio(customHeaders: {
    {% for header in service.headers %}
    '{{ header.title }}': {{ header.value }},
    {% endfor %}
  });
  return {{ service.name_pascal_case }}ApiService(dio, baseUrl: '{{ service.base_url }}');
}