import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_layout.dart';
import '../services/my_environments_service.dart';
import '../widgets/custom_card.dart';

class MyEnvironmentsPage extends StatefulWidget {
  const MyEnvironmentsPage({super.key});

  @override
  State<MyEnvironmentsPage> createState() => _MyEnvironmentsPageState();
}

class _MyEnvironmentsPageState extends State<MyEnvironmentsPage> {
  final MyEnvironmentsService _myEnvironmentsService = MyEnvironmentsService();
  
  List<Map<String, dynamic>> _savedEnvironments = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadSavedEnvironments();
  }

  Future<void> _loadSavedEnvironments() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final environments = await _myEnvironmentsService.getSavedEnvironments();
      setState(() {
        _savedEnvironments = environments;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      print('Error loading saved environments: $e');
    }
  }

  Future<void> _removeEnvironment(Map<String, dynamic> environment) async {
    try {
      await _myEnvironmentsService.removeEnvironment(environment['id']);
      setState(() {
        _savedEnvironments.removeWhere((env) => env['id'] == environment['id']);
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Ortam verisi kaldırıldı',
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: AppTheme.primaryColor,
          duration: const Duration(seconds: 2),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Ortam verisi kaldırılırken hata oluştu: $e'),
          backgroundColor: AppTheme.errorColor,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppLayout(
      currentPageIndex: 4, // My Environments index
      pageTitle: 'Ortamlarım',
      child: SafeArea(
        child: Column(
          children: [
            // Header with Add Environment Button
            Container(
              padding: const EdgeInsets.all(AppTheme.paddingLarge),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      'Kayıtlı Ortam Verilerim',
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeXLarge,
                        fontWeight: AppTheme.fontWeightBold,
                        color: AppTheme.textPrimaryColor,
                      ),
                    ),
                  ),
                  const SizedBox(width: AppTheme.paddingMedium), // Spacing eklendi
                  ElevatedButton.icon(
                    onPressed: () {
                      AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
                    },
                    icon: const Icon(Icons.add, size: 16), // Icon boyutu küçültüldü
                    label: const Text('Yeni Ortam Ekle'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryColor,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppTheme.paddingMedium, // Padding küçültüldü
                        vertical: AppTheme.paddingSmall,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            
            // Content
            Expanded(
              child: _isLoading
                  ? const Center(
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primaryColor),
                      ),
                    )
                  : _savedEnvironments.isEmpty
                      ? _buildEmptyState()
                      : _buildEnvironmentsList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.eco_outlined,
            size: 80,
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
          ),
          const SizedBox(height: AppTheme.paddingLarge),
          Text(
            'Henüz kayıtlı ortam veriniz yok',
            style: TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightMedium,
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingSmall),
          Text(
            'Ortam koşullarından ürün önerisi alarak\nortam verilerinizi buraya ekleyebilirsiniz',
            textAlign: TextAlign.center,
            style: AppTheme.bodyStyle.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingXLarge),
          ElevatedButton.icon(
            onPressed: () {
              AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
            },
            icon: const Icon(Icons.add),
            label: const Text('Ortam Ekle'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(
                horizontal: AppTheme.paddingXLarge,
                vertical: AppTheme.paddingMedium,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEnvironmentsList() {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: AppTheme.paddingLarge),
      itemCount: _savedEnvironments.length,
      itemBuilder: (context, index) {
        final environment = _savedEnvironments[index];
        return Padding(
          padding: const EdgeInsets.only(bottom: AppTheme.paddingLarge),
          child: _buildEnvironmentCard(environment),
        );
      },
    );
  }

  Widget _buildEnvironmentCard(Map<String, dynamic> environment) {
    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header with title and remove button
          Row(
            children: [
              Expanded(
                child: Text(
                  'Ortam Verisi #${environment['id']}',
                  style: const TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
              ),
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: AppTheme.errorColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: IconButton(
                  onPressed: () => _removeEnvironment(environment),
                  icon: const Icon(
                    Icons.delete_outline,
                    color: AppTheme.errorColor,
                    size: 20,
                  ),
                  padding: EdgeInsets.zero,
                ),
              ),
            ],
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          // Environment data grid
          _buildEnvironmentDataGrid(environment),
          
          const SizedBox(height: AppTheme.paddingMedium),
          
          // Footer with date
          Row(
            children: [
              Icon(
                Icons.calendar_today,
                size: 14,
                color: AppTheme.textSecondaryColor,
              ),
              const SizedBox(width: AppTheme.paddingSmall),
              Text(
                'Eklendi: ${_formatDate(DateTime.parse(environment['createdAt']))}',
                style: AppTheme.bodyStyle.copyWith(
                  color: AppTheme.textSecondaryColor,
                  fontSize: AppTheme.fontSizeSmall,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildEnvironmentDataGrid(Map<String, dynamic> environment) {
    final data = environment['data'];
    
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      crossAxisSpacing: AppTheme.paddingMedium,
      mainAxisSpacing: AppTheme.paddingMedium,
      childAspectRatio: 3,
      children: [
        _buildDataItem('pH', data['ph']?.toString() ?? 'N/A'),
        _buildDataItem('Azot (ppm)', data['nitrogen']?.toString() ?? 'N/A'),
        _buildDataItem('Fosfor (ppm)', data['phosphorus']?.toString() ?? 'N/A'),
        _buildDataItem('Potasyum (ppm)', data['potassium']?.toString() ?? 'N/A'),
        _buildDataItem('Nem (%)', data['humidity']?.toString() ?? 'N/A'),
        _buildDataItem('Sıcaklık (°C)', data['temperature']?.toString() ?? 'N/A'),
        _buildDataItem('Yağış (mm)', data['rainfall']?.toString() ?? 'N/A'),
        _buildDataItem('Bölge', data['region']?.toString() ?? 'N/A'),
      ],
    );
  }

  Widget _buildDataItem(String label, String value) {
    return Container(
      height: 60, // Yükseklik daha da artırıldı
      padding: const EdgeInsets.all(6), // Padding azaltıldı
      decoration: BoxDecoration(
        color: AppTheme.primaryLightColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
        border: Border.all(
          color: AppTheme.primaryLightColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: AppTheme.bodyStyle.copyWith(
              color: AppTheme.textSecondaryColor,
              fontSize: 11, // Font boyutu küçültüldü
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: const TextStyle(
              fontSize: 12, // Font boyutu küçültüldü
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}
