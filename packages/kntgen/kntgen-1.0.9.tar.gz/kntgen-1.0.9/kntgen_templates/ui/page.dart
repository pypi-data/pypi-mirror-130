import 'package:flutter/material.dart';
import 'package:knt_ui/knt_ui.dart';
import 'package:{{ package_name }}/resources.dart';

// TODO: Import tabs widget path here

class {{ page.name }}Page extends StatefulWidget {
  const {{ page.name }}({Key? key}) : super(key: key);

  @override
  State<{{ page.name }}Page> createState() => _{{ page.name }}PageState();
}

class _{{ page.name }}PageState extends State<{{ page.name }}Page> {
  final _onTabChanged = ValueNotifier<int>(0);

  @override
  Widget build(BuildContext context) {
    final tabPresents = TabIconMain.values;
    return KntBottomNavScaffold(
      onTabChanged: _onTabChanged,
      appBar: KntAppBar(titlePage: '{empty title}'),
      icons: tabPresents,
      tabs: List.generate(
        tabPresents.length,
            (index) => Container(child:Center(child: Text(
                tabPresents[index].localeKeyTitle.tr(),
              style: TextStyle(
                color: Colors.black,
                fontSize: 24.sp,
              ),
            ),),),
      ),
    );
  }
}

abstract class TabIcon{{ page.name }} {
  {% for tab in page.tabs %}
  static final TabIcon home = TabIcon(
    localeKeyTitle: {{ tab.locale_key }},
    activeImagePath: {{ tab.active_image }},
    inactiveImagePath: {{ tab.inactive_image }},
  );
  {% endfor %}

  static final List<TabIcon> values = [
    {% for tab in page.tabs %}
    {{tab.name}},
    {% endfor %}
  ];
}
