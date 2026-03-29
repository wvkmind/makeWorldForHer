import 'package:flutter_test/flutter_test.dart';
import 'package:xiaoai_app/main.dart';

void main() {
  testWidgets('App starts', (WidgetTester tester) async {
    await tester.pumpWidget(const XiaoaiApp());
    expect(find.text('客厅'), findsOneWidget);
  });
}
