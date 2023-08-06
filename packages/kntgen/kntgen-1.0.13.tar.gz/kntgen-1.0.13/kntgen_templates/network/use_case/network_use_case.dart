import 'package:injectable/injectable.dart';

import '../../repo/cloud_repo.dart';
import 'core/base_use_case.dart';

@injectable
class {{ api.name_pascal_case }}UseCase implements UseCase<{{ api.request_type_pascal_case }}, {{ api.response_type_pascal_case }}> {
  final CloudRepo _repo;

  const {{ api.name_pascal_case }}UseCase(this._repo);

  @override
  Future<{{ api.response_type_pascal_case }}> call({{ api.request_type_pascal_case }} params) async {
    return await _repo.{{ api.name_camel_case }}(params);
  }
}
{{ '' }}