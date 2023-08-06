import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:test/test.dart';
import 'package:{{ package_name }}/bloc/{{ bloc.bloc_name_snake_case }}_bloc.dart';

void main() {
  test{{ bloc.name }}Bloc();
}

/// This test function could be imported into other unit_test/integration_test scripts
void test{{ bloc.name }}Bloc() {
  group('🧪🧪🧪🧪🧪 Testing: {{ bloc.name }}Bloc 🧪🧪🧪🧪🧪', () {
    setUp(() {
      // Initialize mock use cases here
    });

    test('¯\\_(ツ)_/¯🧪 Initial state is BaseInitState', () {
      expect(
        {{ bloc.name }}Bloc().state,
        isA<BaseInitState>(),
      );
    });

    blocTest<BaseEvent, BaseState>(
      '¯\\_(ツ)_/¯🧪 Emits [] when nothing is added',
      build: () => {{ bloc.name }}Bloc(),
      expect: () => const <BaseState>[],
    );

    {% for event in bloc.events %}
    blocTest<BaseEvent, BaseState>(
      '¯\\_(ツ)_/¯🧪 Emits [{% for willBeEmittedState in event.emit %}isA<{{ willBeEmittedState }}State>(){{ ', ' if not loop.last }}{% endfor %}] when [{{ event.name }}Event] is added',
      build: () {
        // Stub the needed use cases
        // when(fetchItemUseCase()).thenAnswer((_) async => []);
        return {{ bloc.name }}Bloc();
      },
      seed: () => BaseInitState(),
      act: (bloc) => bloc.add({{ event.name }}Event()),
      wait: Duration.zero,
      skip: 0,
      expect: () => const <BaseState>[
        {% for willBeEmittedState in event.emit %}
        isA<{{ willBeEmittedState }}State>(),
        {% endfor %}
      ],
      errors: () => [isA<Exception>()],
      verify: (_) {
        // Verify internal bloc functionality
        // verify(
        //   () => addItemUseCase(),
        // ).called(1);
        // verify(fetchItemUseCase()).called(1);
      },
    );
    {{- '\n' if not loop.last }}
    {% endfor %}
  });
}
{{ '' }}