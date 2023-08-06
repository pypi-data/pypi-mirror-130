# Code generator for Appixi Flutter Applications
## Installation:
### Install using pip3:
Open Terminal and run:
``
$ brew install python
``
``
$ pip3 install kntgen
``

### Update:

``
$ pip3 install -U kntgen
``

### Uninstall:

``
$ pip3 uninstall kntgen
``

### Roadmap:

[x] Support STACK_VIEW type? Could check stack with z-axis and order in [children]

[ ] Detect SingleChildScrollView with [overflowDirection] after adding scroll prototype for a [Frame]

[ ] View could be expanded in row/column? Normally (fixed) tv, tf will take the expansion

[ ] Could gen rich text? Using ['characterStyleOverrides']

[ ] Also gen shimmer loading for item?

[ ] Gen model and mock model Dart class?

[x] Printout to console/preview how the new generated widget/item looks like, before let users confirm they want to generate it?

[ ] Read file en-US.json before generate string in widget/item?

[ ] Generate paging widget? End withs {_paging} postfix, only apply for lv and gv

[ ] Printout invalid named node with node id

[ ] Auto detect same view to generate lv, gv? No need?

[ ] Auto detect background view type (check rect ~ outer rect with bias)?

[ ] From prototype generate navigation? -> Using node id 0:1 and search transitionNodeID