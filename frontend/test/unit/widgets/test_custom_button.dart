/**
 * Unit tests for CustomButton widget
 * 
 * Bu test dosyası CustomButton widget'ı için birim testlerini içerir.
 */

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:terramind_app/widgets/custom_button.dart';

void main() {
  group('CustomButton Tests', () {
    testWidgets('should render button with text', (WidgetTester tester) async {
      // Test basic button rendering
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Test Button',
              onPressed: () {},
            ),
          ),
        ),
      );

      // Verify button is rendered
      expect(find.text('Test Button'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('should call onPressed when tapped', (WidgetTester tester) async {
      // Test button tap functionality
      bool wasPressed = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Test Button',
              onPressed: () {
                wasPressed = true;
              },
            ),
          ),
        ),
      );

      // Tap the button
      await tester.tap(find.text('Test Button'));
      await tester.pump();

      // Verify onPressed was called
      expect(wasPressed, isTrue);
    });

    testWidgets('should be disabled when onPressed is null', (WidgetTester tester) async {
      // Test disabled button state
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Disabled Button',
              onPressed: null,
            ),
          ),
        ),
      );

      // Verify button is disabled
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.onPressed, isNull);
    });

    testWidgets('should show loading state', (WidgetTester tester) async {
      // Test loading state
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Loading Button',
              onPressed: () {},
              isLoading: true,
            ),
          ),
        ),
      );

      // Verify loading indicator is shown
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      
      // Verify original text is not shown
      expect(find.text('Loading Button'), findsNothing);
    });

    testWidgets('should apply custom width', (WidgetTester tester) async {
      // Test custom width
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Wide Button',
              onPressed: () {},
              width: 200.0,
            ),
          ),
        ),
      );

      // Verify button has custom width
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.minimumSize?.resolve({}), equals(Size(200.0, 48.0)));
    });

    testWidgets('should apply custom height', (WidgetTester tester) async {
      // Test custom height
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Tall Button',
              onPressed: () {},
              height: 60.0,
            ),
          ),
        ),
      );

      // Verify button has custom height
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.minimumSize?.resolve({}), equals(Size(200.0, 60.0)));
    });

    testWidgets('should apply primary style', (WidgetTester tester) async {
      // Test primary button style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Primary Button',
              onPressed: () {},
              style: CustomButtonStyle.primary,
            ),
          ),
        ),
      );

      // Verify button has primary style
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.backgroundColor?.resolve({}), equals(Colors.green));
    });

    testWidgets('should apply secondary style', (WidgetTester tester) async {
      // Test secondary button style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Secondary Button',
              onPressed: () {},
              style: CustomButtonStyle.secondary,
            ),
          ),
        ),
      );

      // Verify button has secondary style
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.backgroundColor?.resolve({}), equals(Colors.grey));
    });

    testWidgets('should apply outline style', (WidgetTester tester) async {
      // Test outline button style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Outline Button',
              onPressed: () {},
              style: CustomButtonStyle.outline,
            ),
          ),
        ),
      );

      // Verify button has outline style
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.backgroundColor?.resolve({}), equals(Colors.transparent));
      expect(button.style?.side?.resolve({})?.color, equals(Colors.green));
    });

    testWidgets('should apply danger style', (WidgetTester tester) async {
      // Test danger button style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Danger Button',
              onPressed: () {},
              style: CustomButtonStyle.danger,
            ),
          ),
        ),
      );

      // Verify button has danger style
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.backgroundColor?.resolve({}), equals(Colors.red));
    });

    testWidgets('should show icon when provided', (WidgetTester tester) async {
      // Test button with icon
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Icon Button',
              onPressed: () {},
              icon: Icons.add,
            ),
          ),
        ),
      );

      // Verify icon is shown
      expect(find.byIcon(Icons.add), findsOneWidget);
      expect(find.text('Icon Button'), findsOneWidget);
    });

    testWidgets('should show only icon when text is empty', (WidgetTester tester) async {
      // Test icon-only button
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: '',
              onPressed: () {},
              icon: Icons.close,
            ),
          ),
        ),
      );

      // Verify only icon is shown
      expect(find.byIcon(Icons.close), findsOneWidget);
      expect(find.text(''), findsNothing);
    });

    testWidgets('should apply custom border radius', (WidgetTester tester) async {
      // Test custom border radius
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Rounded Button',
              onPressed: () {},
              borderRadius: 20.0,
            ),
          ),
        ),
      );

      // Verify button has custom border radius
      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.style?.shape?.resolve({}), isA<RoundedRectangleBorder>());
    });

    testWidgets('should handle long text properly', (WidgetTester tester) async {
      // Test button with long text
      const longText = 'This is a very long button text that should be handled properly';
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: longText,
              onPressed: () {},
            ),
          ),
        ),
      );

      // Verify long text is displayed
      expect(find.text(longText), findsOneWidget);
    });

    testWidgets('should maintain accessibility', (WidgetTester tester) async {
      // Test accessibility features
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Accessible Button',
              onPressed: () {},
            ),
          ),
        ),
      );

      // Verify button is accessible
      expect(find.byType(ElevatedButton), findsOneWidget);
      
      // Verify semantic label is set
      expect(find.bySemanticsLabel('Accessible Button'), findsOneWidget);
    });

    testWidgets('should handle rapid taps', (WidgetTester tester) async {
      // Test rapid tapping
      int tapCount = 0;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Rapid Tap Button',
              onPressed: () {
                tapCount++;
              },
            ),
          ),
        ),
      );

      // Tap multiple times rapidly
      for (int i = 0; i < 5; i++) {
        await tester.tap(find.text('Rapid Tap Button'));
        await tester.pump();
      }

      // Verify all taps were registered
      expect(tapCount, equals(5));
    });

    testWidgets('should work with different themes', (WidgetTester tester) async {
      // Test button with different theme
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple),
          ),
          home: Scaffold(
            body: CustomButton(
              text: 'Themed Button',
              onPressed: () {},
            ),
          ),
        ),
      );

      // Verify button renders with theme
      expect(find.text('Themed Button'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });
  });
}
