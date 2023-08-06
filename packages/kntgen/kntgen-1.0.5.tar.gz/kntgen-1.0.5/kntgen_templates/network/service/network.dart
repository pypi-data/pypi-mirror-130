{{ '' }}
@RestApi()
abstract class {{ service.name_pascal_case }}ApiService {
  factory {{ service.name_pascal_case }}ApiService(Dio dio, {String baseUrl}) = _{{ service.name_pascal_case }}ApiService;
  {% for api in service.apis %}
  {{ '' }}
  {{ api.retrofit_endpoint }}
  {% if api.static_headers|length > 0 %}
  @Headers(<String, dynamic>{
    {% for header in api.static_headers %}
    '{{ header.title }}': {{ header.value }},
    {% endfor %}
  })
  {% endif %}
  {% if api.has_fields %}
  @FormUrlEncoded()
  {% endif %}
  Future<{{ api.response_type_pascal_case }}> {{ api.name_camel_case }}(
    {% for header in api.dynamic_headers %}
    @Header('{{ header.title }}') {{ header.content_type }} {{ header.title_camel_case}},
    {% endfor %}
    {% for path, path_camel_case in api.path_from_endpoint.items() %}
    @Path('{{ path }}') String {{ path_camel_case }},
    {% endfor %}
    {% if api.queries|length > 0 %}
    @Queries() Map<String, dynamic> queries,
    {% endif %}
    {% if api.body|length > 0 %}
    @Body() Map<String, dynamic> body,
    {% endif %}
    {% for field in api.fields %}
    @Field('{{ field.title }}') {{ field.content_type }} {{ field.title_camel_case }},
    {% endfor %}
    {% for part in api.parts %}
    @Part(name: '{{ part.title }}') {{ part.content_type }} {{ part.title_camel_case }},
    {% endfor %}
  );
  {% endfor %}
}
{{ '' }}