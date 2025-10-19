/**
 * Unit tests for CustomCard widget
 * 
 * Bu test dosyası CustomCard widget'ı için birim testlerini içerir.
 */

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:terramind_app/widgets/custom_card.dart';

void main() {
  group('CustomCard Tests', () {
    testWidgets('should render card with child content', (WidgetTester tester) async {
      // Test basic card rendering
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify card and content are rendered
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should render card with title', (WidgetTester tester) async {
      // Test card with title
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Test Title',
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify title and content are rendered
      expect(find.text('Test Title'), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should render card with subtitle', (WidgetTester tester) async {
      // Test card with subtitle
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Test Title',
              subtitle: 'Test Subtitle',
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify title, subtitle and content are rendered
      expect(find.text('Test Title'), findsOneWidget);
      expect(find.text('Test Subtitle'), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should render card with action button', (WidgetTester tester) async {
      // Test card with action button
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Test Title',
              child: Text('Test Content'),
              actionText: 'Action',
              onActionPressed: () {},
            ),
          ),
        ),
      );

      // Verify action button is rendered
      expect(find.text('Action'), findsOneWidget);
      expect(find.byType(TextButton), findsOneWidget);
    });

    testWidgets('should call onActionPressed when action button is tapped', (WidgetTester tester) async {
      // Test action button tap functionality
      bool wasPressed = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Test Title',
              child: Text('Test Content'),
              actionText: 'Action',
              onActionPressed: () {
                wasPressed = true;
              },
            ),
          ),
        ),
      );

      // Tap the action button
      await tester.tap(find.text('Action'));
      await tester.pump();

      // Verify onActionPressed was called
      expect(wasPressed, isTrue);
    });

    testWidgets('should apply custom padding', (WidgetTester tester) async {
      // Test custom padding
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              padding: EdgeInsets.all(20.0),
            ),
          ),
        ),
      );

      // Verify card is rendered with custom padding
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should apply custom margin', (WidgetTester tester) async {
      // Test custom margin
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              margin: EdgeInsets.all(16.0),
            ),
          ),
        ),
      );

      // Verify card is rendered with custom margin
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should apply custom elevation', (WidgetTester tester) async {
      // Test custom elevation
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              elevation: 8.0,
            ),
          ),
        ),
      );

      // Verify card has custom elevation
      final card = tester.widget<Card>(find.byType(Card));
      expect(card.elevation, equals(8.0));
    });

    testWidgets('should apply custom border radius', (WidgetTester tester) async {
      // Test custom border radius
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              borderRadius: 20.0,
            ),
          ),
        ),
      );

      // Verify card has custom border radius
      final card = tester.widget<Card>(find.byType(Card));
      expect(card.shape, isA<RoundedRectangleBorder>());
    });

    testWidgets('should apply primary style', (WidgetTester tester) async {
      // Test primary card style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              style: CustomCardStyle.primary,
            ),
          ),
        ),
      );

      // Verify card is rendered with primary style
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should apply secondary style', (WidgetTester tester) async {
      // Test secondary card style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              style: CustomCardStyle.secondary,
            ),
          ),
        ),
      );

      // Verify card is rendered with secondary style
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should apply outlined style', (WidgetTester tester) async {
      // Test outlined card style
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              child: Text('Test Content'),
              style: CustomCardStyle.outlined,
            ),
          ),
        ),
      );

      // Verify card is rendered with outlined style
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
    });

    testWidgets('should handle long title text', (WidgetTester tester) async {
      // Test card with long title
      const longTitle = 'This is a very long title that should be handled properly by the card widget';
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: longTitle,
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify long title is displayed
      expect(find.text(longTitle), findsOneWidget);
    });

    testWidgets('should handle long subtitle text', (WidgetTester tester) async {
      // Test card with long subtitle
      const longSubtitle = 'This is a very long subtitle that should be handled properly by the card widget';
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Test Title',
              subtitle: longSubtitle,
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify long subtitle is displayed
      expect(find.text(longSubtitle), findsOneWidget);
    });

    testWidgets('should handle complex child widget', (WidgetTester tester) async {
      // Test card with complex child widget
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Complex Card',
              child: Column(
                children: [
                  Text('First Line'),
                  Text('Second Line'),
                  Icon(Icons.star),
                  ElevatedButton(
                    onPressed: () {},
                    child: Text('Button'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify all child elements are rendered
      expect(find.text('Complex Card'), findsOneWidget);
      expect(find.text('First Line'), findsOneWidget);
      expect(find.text('Second Line'), findsOneWidget);
      expect(find.byIcon(Icons.star), findsOneWidget);
      expect(find.text('Button'), findsOneWidget);
    });

    testWidgets('should handle null action button', (WidgetTester tester) async {
      // Test card without action button
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'No Action Card',
              child: Text('Test Content'),
            ),
          ),
        ),
      );

      // Verify no action button is rendered
      expect(find.text('No Action Card'), findsOneWidget);
      expect(find.text('Test Content'), findsOneWidget);
      expect(find.byType(TextButton), findsNothing);
    });

    testWidgets('should maintain accessibility', (WidgetTester tester) async {
      // Test accessibility features
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Accessible Card',
              child: Text('Accessible Content'),
            ),
          ),
        ),
      );

      // Verify card is accessible
      expect(find.byType(Card), findsOneWidget);
      expect(find.text('Accessible Card'), findsOneWidget);
      expect(find.text('Accessible Content'), findsOneWidget);
    });

    testWidgets('should work with different themes', (WidgetTester tester) async {
      // Test card with different theme
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple),
          ),
          home: Scaffold(
            body: CustomCard(
              title: 'Themed Card',
              child: Text('Themed Content'),
            ),
          ),
        ),
      );

      // Verify card renders with theme
      expect(find.text('Themed Card'), findsOneWidget);
      expect(find.text('Themed Content'), findsOneWidget);
      expect(find.byType(Card), findsOneWidget);
    });

    testWidgets('should handle multiple cards', (WidgetTester tester) async {
      // Test multiple cards
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                CustomCard(
                  title: 'First Card',
                  child: Text('First Content'),
                ),
                CustomCard(
                  title: 'Second Card',
                  child: Text('Second Content'),
                ),
              ],
            ),
          ),
        ),
      );

      // Verify both cards are rendered
      expect(find.text('First Card'), findsOneWidget);
      expect(find.text('First Content'), findsOneWidget);
      expect(find.text('Second Card'), findsOneWidget);
      expect(find.text('Second Content'), findsOneWidget);
      expect(find.byType(Card), findsNWidgets(2));
    });

    testWidgets('should handle empty child', (WidgetTester tester) async {
      // Test card with empty child
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomCard(
              title: 'Empty Card',
              child: SizedBox.shrink(),
            ),
          ),
        ),
      );

      // Verify card is rendered even with empty child
      expect(find.text('Empty Card'), findsOneWidget);
      expect(find.byType(Card), findsOneWidget);
    });
  });
}
