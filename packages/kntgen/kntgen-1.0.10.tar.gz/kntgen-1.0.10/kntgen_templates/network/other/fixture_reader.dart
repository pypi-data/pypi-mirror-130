import 'dart:convert';
import 'dart:io';

String fixtureJson(String fileName) =>
    File('test/fixtures/$fileName').readAsStringSync();

Map<String, dynamic> fixtureMap(String fileName) =>
    jsonDecode(fixtureJson(fileName));
{{ '' }}