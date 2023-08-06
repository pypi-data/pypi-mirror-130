{{ '' }}
@JsonSerializable()
class {{ model_name }} {
  {% for p in properties %}
  @JsonKey(name: '{{ p.raw_name }}'{% if not p.is_optional %}, defaultValue: {{ p.value }}{% endif %})
  final {{ p.type_name }} {{ p.name }};
  {{- '\n' if loop.last }}
  {% endfor %}
  {% if properties|length > 0 %}
  const {{ model_name }}({
    {% for p in properties %}
    this.{{ p.name }}{% if not p.is_optional %} = {{ p.value }}{% endif %},
    {% endfor %}
  });

  {% endif %}
  factory {{ model_name }}.fromJson(Map<String, dynamic> json) => _${{ model_name }}FromJson(json);

  Map<String, dynamic> toJson() => _${{ model_name }}ToJson(this);
}