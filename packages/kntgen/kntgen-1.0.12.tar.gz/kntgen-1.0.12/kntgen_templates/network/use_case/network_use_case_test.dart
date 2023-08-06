{% if api.has_file_part %}
import 'dart:io';
{% endif %}
import 'package:injectable/injectable.dart';

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:{{ package_name }}/data/network/api_service.dart';
import 'package:{{ package_name }}/data/repo/data_cloud_repo.dart';
import 'package:{{ package_name }}/model/network_models.dart';
import 'package:{{ package_name }}/use_case/core/base_use_case.dart';
import 'package:{{ package_name }}/use_case/{{ api.name_snake_case }}.dart';

import '{{ api.name_snake_case }}_use_case_test.mocks.dart';

@GenerateMocks([{{ service.name_pascal_case }}ApiService, DataCloudRepo])
void main() {
  late Mock{{ service.name_pascal_case }}ApiService service;
  late MockDataCloudRepo repo;
  late {{ api.name_pascal_case }}UseCase useCase;

  setUp(() {
    service = Mock{{ service.name_pascal_case }}ApiService();
    repo = MockDataCloudRepo();
    usecase = {{ api.name_pascal_case }}UseCase(repo);
  });

  group('🧪🧪🧪🧪🧪 Testing: {{ api.name_pascal_case }}UseCase 🧪🧪🧪🧪🧪', () async {
    final tRequest = {{ api.request_type_pascal_case }}(
      {% for path_camel_case in api.path_from_endpoint.values() %}
      {{ path_camel_case}}: '{{ path_camel_case}}',
      {% endfor %}
      {% for header in api.dynamic_headers %}
      {{ header.title_camel_case }}: {{ header.non_null_value }},
      {% endfor %}
      {% for query in api.queries %}
      {{ query.title_camel_case }}: {{ query.non_null_value }},
      {% endfor %}
      {% for b in api.body %}
      {{ b.title_camel_case }}: {{ b.non_null_value }},
      {% endfor %}
      {% for field in api.fields %}
      {{ field.title_camel_case }}: {{ field.non_null_value }},
      {% endfor %}
      {% for part in api.parts %}
      {{ part.title_camel_case }}: {{ part.non_null_value }},
      {% endfor %}
    );

    test('¯\\_(ツ)_/¯🧪 Should {{ api.name_to_word }} with correct given [{{ api.request_type_pascal_case }}]\'s params, then return [{{ api.response_type_pascal_case }}]', () async {
        // Arrange
        when(service.{{ api.name_camel_case }}(
            {% for header in api.dynamic_headers %}
            any,
            {% endfor %}
            {% for path_camel_case in api.path_from_endpoint.values() %}
            any,
            {% endfor %}
            {% if api.queries|length > 0 %}
            any,
            {% endif %}
            {% if api.body|length > 0 %}
            any,
            {% endif %}
            {% for field in api.fields %}
            any,
            {% endfor %}
            {% for part in api.parts %}
            any,
            {% endfor %}
        ))
            .thenAnswer((_) async => {{ api.response_type_pascal_case }}.fromJson(fixtureMap('{{ api.response_type_snake_case }}.json')));
        // Act
        final result = await usecase(tRequest);
        // Assert
        expect(result, isA<{{ api.response_type_pascal_case }}>());
        verify(service.{{ api.name_camel_case }}(
          {% for header in api.dynamic_headers %}
          tRequest.headers.{{ header.title_camel_case}},
          {% endfor %}
          {% for path_camel_case in api.path_from_endpoint.values() %}
          tRequest.paths.{{ path_camel_case }},
          {% endfor %}
          {% if api.queries|length > 0 %}
          tRequest.queries.toJson(),
          {% endif %}
          {% if api.body|length > 0 %}
          tRequest.body,
          {% endif %}
          {% for field in api.fields %}
          tRequest.fields.{{ field.title_camel_case }},
          {% endfor %}
          {% for part in api.parts %}
          {% if part.is_file_type %}
          {% if part.is_list_type %}
          tRequest.parts.{{ part.title_camel_case }}.map((filePath) => File(filePath)).toList(),
          {% else %}
          File(tRequest.parts.{{ part.title_camel_case }}),
          {% endif %}
          {% else %}
          tRequest.parts.{{ part.title_camel_case }},
          {% endif %}
          {% endfor %}
        ));
        verify(repo.{{ api.name_camel_case }}(tRequest));
        verifyNoMoreInteractions(repo);
      },
    );
  });
}
{{ '' }}