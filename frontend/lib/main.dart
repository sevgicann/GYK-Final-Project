import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';
import 'core/navigation/app_router.dart';

void main() {
  runApp(const TerramindApp());
}

class TerramindApp extends StatelessWidget {
  const TerramindApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Terramind',
      theme: AppTheme.lightTheme,
      initialRoute: AppRouter.register,
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
