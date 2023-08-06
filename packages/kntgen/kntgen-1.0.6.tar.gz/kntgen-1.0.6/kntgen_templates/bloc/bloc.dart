import 'package:injectable/injectable.dart';
import 'package:knt_bloc/knt_bloc.dart';

{% if bloc.need_singleton %}@singleton{% else %}@injectable{% endif +%}
class {{ bloc.name }}Bloc extends {% if bloc.need_cloud %}BaseApiBloc{% else %}BaseBloc{% endif %} {
  @override
  Stream<BaseState> handleEvent(BaseEvent event) async* {
    yield* super.handleEvent(event);
    switch (event.runtimeType) {
      {% for event in bloc.events %}
      case {{ event.name }}Event:
        yield* _handle{{ event.name }}Event(event as {{ event.name }}Event);
        break;
      {{- '\n' if not loop.last }}
      {% endfor %}
    }
  }
  {% if bloc.need_custom_error %}

  /// Override this method if we need throw customized states instead of [BaseErrorState]
  ///
  /// For example, with custom tag from event we could throw customized states:
  ///
  /// ```dart
  /// @override
  /// Stream<BaseState> handleBaseErrorEvent(BaseErrorEvent event) async* {
  ///   if (event.tag == (FetchFromCloudEvent).toString()) {
  ///     yield FetchedFromCloudFailureState();
  ///     return;
  ///   }
  ///   yield* super.handleBaseErrorEvent(event);
  /// }
  /// ```
  @override
  Stream<BaseState> handleBaseErrorEvent(BaseErrorEvent event) async* {
    yield* super.handleBaseErrorEvent(event);
  }
  {% endif %}
  {% for event in bloc.events %}

  Stream<BaseState> _handle{{ event.name }}Event({{ event.name }}Event event) async* {
    // Processing
    {% for willBeEmittedState in event.emit %}
    yield {{ willBeEmittedState }}State();
    {% endfor %}
  }
  {% endfor %}
}

// region EVENT
{% for event in bloc.events %}
class {{ event.name }}Event extends BaseEvent {
  {% for param in event.params %}
  final {{ param.type_name }} {{ param.name }};
  {{- '\n' if loop.last }}
  {% endfor %}
  const {{ event.name }}Event({
    {% for param in event.params %}
    {%+ if param.type_name.strip()[-1] != '?' and not param.default_value %}required {% endif %}this.{{ param.name }}{% if param.default_value %} = {{ param.default_value }}{% endif %},
    {% endfor %}
  });
  {% if event.need_check_connection %}

  @override
  bool get needCheckConnection => true;
  {% endif %}
}
{{- '\n' if not loop.last }}
{% endfor %}
// endregion

// region STATE
{% for state in bloc.states %}
class {{ state.name }}State extends {% if state.is_error %}BaseErrorState{% else %}BaseState{% endif %} {
  {% for param in state.params %}
  final {{ param.type_name }} {{ param.name }};
  {{- '\n' if loop.last }}
  {% endfor %}
  {% if state.params|length > 0 %}
  const {{ state.name }}State({
    {% for param in state.params %}
    {%+ if param.type_name.strip()[-1] != '?' and not param.default_value %}required {% endif %}this.{{ param.name }}{% if param.default_value %} = {{ param.default_value }}{% endif %},
    {% endfor %}
  }){% if state.is_error %} : super(exception: KntException(KntIssue.undefined)){% endif %};
  {% endif %}
}
{{- '\n' if not loop.last }}
{% endfor %}
// endregion
{{ '' }}