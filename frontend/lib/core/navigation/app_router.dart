import 'package:flutter/material.dart';
import '../../pages/register_page.dart';
import '../../pages/login_page.dart';
import '../../pages/home_page.dart';
import '../../pages/product_selection_page.dart';
import '../../pages/environment_recommendation_page.dart';

class AppRouter {
  static const String register = '/register';
  static const String login = '/login';
  static const String home = '/home';
  static const String productSelection = '/product-selection';
  static const String environmentRecommendation = '/environment-recommendation';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case register:
        return MaterialPageRoute(
          builder: (_) => const RegisterPage(),
          settings: settings,
        );
      
      case login:
        return MaterialPageRoute(
          builder: (_) => const LoginPage(),
          settings: settings,
        );
      
      case home:
        return MaterialPageRoute(
          builder: (_) => const HomePage(),
          settings: settings,
        );
      
      case productSelection:
        return MaterialPageRoute(
          builder: (_) => const ProductSelectionPage(),
          settings: settings,
        );
      
      case environmentRecommendation:
        return MaterialPageRoute(
          builder: (_) => const EnvironmentRecommendationPage(),
          settings: settings,
        );
      
      default:
        return MaterialPageRoute(
          builder: (_) => const RegisterPage(),
          settings: settings,
        );
    }
  }

  static void navigateTo(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushNamed(context, routeName, arguments: arguments);
  }

  static void navigateAndReplace(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushReplacementNamed(context, routeName, arguments: arguments);
  }

  static void navigateAndClearStack(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushNamedAndRemoveUntil(
      context,
      routeName,
      (route) => false,
      arguments: arguments,
    );
  }

  static void goBack(BuildContext context, {dynamic result}) {
    Navigator.pop(context, result);
  }

  static void goBackTo(BuildContext context, String routeName) {
    Navigator.popUntil(context, ModalRoute.withName(routeName));
  }
}

class RouteArguments {
  final Map<String, dynamic> _arguments;

  RouteArguments(this._arguments);

  T? get<T>(String key) {
    return _arguments[key] as T?;
  }

  T getRequired<T>(String key) {
    final value = _arguments[key] as T?;
    if (value == null) {
      throw ArgumentError('Required argument $key not found');
    }
    return value;
  }

  bool has(String key) {
    return _arguments.containsKey(key);
  }
}
