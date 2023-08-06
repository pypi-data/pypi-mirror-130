{% if api.body|length > 0 %}
import 'package:json_annotation/json_annotation.dart';

part '{{ api.request_type_snake_case }}.g.dart';

{% endif %}
class {{ api.request_type_pascal_case }} {
  {% if api.path_from_endpoint|length > 0 %}
  late _Paths paths;
  {% endif %}
  {% if api.dynamic_headers|length > 0 %}
  late _Headers headers;
  {% endif %}
  {% if api.queries|length > 0 %}
  late _Queries queries;
  {% endif %}
  {% if api.body|length > 0 %}
  late _Body body;
  {% endif %}
  {% if api.fields|length > 0 %}
  late _Fields fields;
  {% endif %}
  {% if api.parts|length > 0 %}
  late _Parts parts;
  {% endif %}
  {% if api.has_param %}
  {{ '' }}
  {{ api.request_type_pascal_case }}({
    {% for path_camel_case in api.path_from_endpoint.values() %}
    required String {{ path_camel_case}},
    {% endfor %}
    {% for header in api.dynamic_headers %}
    {%+ if not header.value %}required {% endif %}{{ header.content_type }} {{ header.title_camel_case }}{% if header.value %} = {{ header.value }}{% endif %},
    {% endfor %}
    {% for query in api.queries %}
    {%+ if not query.value %}required {% endif %}{{ query.content_type }} {{ query.title_camel_case }}{% if query.value %} = {{ query.value }}{% endif %},
    {% endfor %}
    {% for b in api.body %}
    {%+ if not b.value %}required {% endif %}{{ b.content_type }} {{ b.title_camel_case }}{% if b.value %} = {{ b.value }}{% endif %},
    {% endfor %}
    {% for field in api.fields %}
    {%+ if not field.value %}required {% endif %}{{ field.content_type }} {{ field.title_camel_case }}{% if field.value %} = {{ field.value }}{% endif %},
    {% endfor %}
    {% for part in api.parts %}
    {% if part.is_file_type %}
    required {% if part.is_list_type %}List<String>{% else %}String{% endif %} {{ part.title_camel_case }}Path,
    {% else %}
    {%+ if not part.value %}required {% endif %}{{ part.content_type }} {{ part.title_camel_case }}{% if part.value %} = {{ part.value }}{% endif %},
    {% endif %}
    {% endfor %}
  }) {
    {% if api.path_from_endpoint|length > 0 %}
    paths = _Paths(
      {% for path_camel_case in api.path_from_endpoint.values() %}
      {{ path_camel_case}}: {{ path_camel_case}},
      {% endfor %}
    );
    {% endif %}
    {% if api.dynamic_headers|length > 0 %}
    headers = _Headers(
      {% for header in api.dynamic_headers %}
      {{ header.title_camel_case }}: {{ header.title_camel_case }},
      {% endfor %}
    );
    {% endif %}
    {% if api.queries|length > 0 %}
    queries = _Queries(
      {% for query in api.queries %}
      {{ query.title_camel_case }}: {{ query.title_camel_case }},
      {% endfor %}
    );
    {% endif %}
    {% if api.body|length > 0 %}
    body = _Body(
      {% for b in api.body %}
      {{ b.title_camel_case }}: {{ b.title_camel_case }},
      {% endfor %}
    );
    {% endif %}
    {% if api.fields|length > 0 %}
    fields = _Fields(
      {% for field in api.fields %}
      {{ field.title_camel_case }}: {{ field.title_camel_case }},
      {% endfor %}
    );
    {% endif %}
    {% if api.parts|length > 0 %}
    parts = _Parts(
      {% for part in api.parts %}
      {% if part.is_file_type %}
      {{ part.title_camel_case }}Path: {{ part.title_camel_case }}Path,
      {% else %}
      {{ part.title_camel_case }}: {{ part.title_camel_case }},
      {% endif %}
      {% endfor %}
    );
    {% endif %}
  }
  {% endif %}
}
{% if api.path_from_endpoint|length > 0 %}
{{ '' }}
class _Paths {
  {% for path_camel_case in api.path_from_endpoint.values() %}
  final String {{ path_camel_case}};
  {% endfor %}

  const _Paths({
    {% for path_camel_case in api.path_from_endpoint.values() %}
    required this.{{ path_camel_case}},
    {% endfor %}
  });
}
{% endif %}
{% if api.dynamic_headers|length > 0 %}
{{ '' }}
class _Headers {
  {% for header in api.dynamic_headers %}
  final {{ header.content_type }} {{ header.title_camel_case}};
  {% endfor %}

  const _Headers({
    {% for header in api.dynamic_headers %}
    {%+ if not header.value %}required {% endif %}this.{{ header.title_camel_case }}{% if header.value %} = {{ header.value }}{% endif %},
    {% endfor %}
  });
}
{% endif %}
{% if api.queries|length > 0 %}
{{ '' }}
class _Queries {
  {% for query in api.queries %}
  final {{ query.content_type }} {{ query.title_camel_case }};
  {% endfor %}

  const _Queries({
    {% for query in api.queries %}
    {%+ if not query.value %}required {% endif %}this.{{ query.title_camel_case }}{% if query.value %} = {{ query.value }}{% endif %},
    {% endfor %}
  });

  Map<String, dynamic> toMap() => <String, dynamic>{
    {% for query in api.queries %}
    '{{ query.title }}': {{ query.title_camel_case }},
    {% endfor %}
  };
}
{% endif %}
{% if api.body|length > 0 %}
{{ '' }}
class _Body {
  {% for b in api.body %}
  final {{ b.content_type }} {{ b.title_camel_case }};
  {% endfor %}

  const _Body({
    {% for b in api.body %}
    {%+ if not b.value %}required {% endif %}this.{{ b.title_camel_case }}{% if b.value %} = {{ b.value }}{% endif %},
    {% endfor %}
  });

  Map<String, dynamic> toMap() => <String, dynamic>{
    {% for b in api.body %}
    '{{ b.title }}': {{ b.title_camel_case }},
    {% endfor %}
  };

  factory {{ api.request_type_pascal_case }}Body.fromJson(Map<String, dynamic> json) => _${{ api.request_type_pascal_case }}BodyFromJson(json);

  Map<String, dynamic> toJson() => _${{ api.request_type_pascal_case }}BodyToJson(this);
}
{% endif %}
{% if api.fields|length > 0 %}
{{ '' }}
class _Fields {
  {% for field in api.fields %}
  final {{ field.content_type }} {{ field.title_camel_case }};
  {% endfor %}

  const _Fields({
    {% for field in api.fields %}
    {%+ if not field.value %}required {% endif %}this.{{ field.title_camel_case }}{% if field.value %} = {{ field.value }}{% endif %},
    {% endfor %}
  });
}
{% endif %}
{% if api.parts|length > 0 %}
{{ '' }}
class _Parts {
  {% for part in api.parts %}
  {% if part.is_file_type %}
  final {% if part.is_list_type %}List<String>{% else %}String{% endif %} {{ part.title_camel_case }}Path;
  {% else %}
  final {{ part.content_type }} {{ part.title_camel_case }};
  {% endif %}
  {% endfor %}

  const _Parts({
    {% for part in api.parts %}
    {% if part.is_file_type %}
    required this.{{ part.title_camel_case }}Path,
    {% else %}
    {%+ if not part.value %}required {% endif %}this.{{ part.title_camel_case }}{% if part.value %} = {{ part.value }}{% endif %},
    {% endif %}
    {% endfor %}
  });
}
{% endif %}
{{ '' }}