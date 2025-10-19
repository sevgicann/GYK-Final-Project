# PDF Generation Setup Guide

This guide explains how to set up and use the PDF generation feature that integrates with the LLM script you provided.

## Features

The PDF generation system provides two types of reports:

1. **Environment Recommendation PDF**: Explains why specific environmental conditions are needed for a given crop
2. **Crop Recommendation PDF**: Analyzes environmental conditions and provides detailed crop recommendations

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The following packages are required for PDF generation:
- `google-generativeai==0.8.3` - For LLM integration
- `fpdf2==2.7.6` - For PDF generation

### 2. Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Google Generative AI API Key (required)
GOOGLE_API_KEY=your_google_api_key_here

# Font path for PDF generation (optional)
FONT_PATH=backend/ttf_files

# Other existing variables...
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=jwt-secret-string
DATABASE_URL=postgresql://postgres:pass.123@localhost:5432/terramind_db
FLASK_ENV=development
```

### 3. Font Files

Ensure the font files are available in `backend/ttf_files/`:
- `calibri.ttf`
- `calibrib.ttf` (bold)

If these files are not available, the system will fall back to default fonts.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
flutter pub get
```

The following packages are required:
- `path_provider: ^2.1.1` - For file system access
- `permission_handler: ^11.0.1` - For storage permissions

### 2. Android Permissions

The Android manifest already includes the necessary permissions for PDF downloads.

## API Endpoints

### Generate Environment Report
```
POST /api/pdf/generate-environment-report
```

Request body:
```json
{
  "crop": "Domates",
  "location": "Amasya",
  "region": "Karadeniz",
  "soil_type": "Kumlu Toprak",
  "irrigation_method": "Damla Sulama",
  "fertilizer_type": "Amonyum Sülfat",
  "sunlight": "Güneşli"
}
```

### Generate Crop Report
```
POST /api/pdf/generate-crop-report
```

Request body:
```json
{
  "location": "Amasya",
  "region": "Karadeniz",
  "soil_type": "Kumlu Toprak",
  "sunlight": "Güneşli",
  "irrigation_method": "Damla Sulama",
  "fertilizer": "Kompost",
  "ph": 6.5,
  "nitrogen": 120,
  "phosphorus": 60,
  "potassium": 225,
  "humidity": 26,
  "temperature": 23,
  "rainfall": 850,
  "top_3_predictions": [
    ["Domates", 0.8],
    ["Mısır", 0.7],
    ["Buğday", 0.6]
  ]
}
```

## Usage

### In the Frontend

1. Navigate to the "Ortam Koşullarından Ürün Tahmini" page
2. Fill in the required environmental data
3. Click "Öneri Al" to get product recommendations
4. In the recommendations bottom sheet, you'll see a "PDF Raporu Oluştur" button
5. Click the button to generate and download the PDF report

### Testing

Run the test script to verify PDF generation:

```bash
cd backend
python test_pdf_generation.py
```

## How It Works

1. **User Input**: User provides environmental data and gets recommendations
2. **LLM Integration**: The system uses Google's Gemini AI to generate detailed explanations
3. **PDF Creation**: The LLM response is formatted into a professional PDF using FPDF
4. **Download**: The PDF is generated and automatically downloaded to the user's device

## LLM Prompts

The system uses two specialized prompts:

1. **Environment Recommendation Prompt**: Focuses on explaining why specific conditions are needed for a crop
2. **Crop Recommendation Prompt**: Analyzes environmental conditions and provides crop-specific advice

Both prompts are designed to generate Turkish content that is farmer-friendly and scientifically accurate.

## Error Handling

The system includes comprehensive error handling:
- API key validation
- LLM response validation
- PDF generation error handling
- File system permission handling
- Network error handling

## File Structure

```
backend/
├── services/
│   └── pdf_service.py          # PDF generation service
├── routes/
│   └── pdf_generation.py       # PDF API endpoints
├── test_pdf_generation.py      # Test script
└── ttf_files/                  # Font files for PDF

frontend/
├── lib/services/
│   └── pdf_service.dart        # Frontend PDF service
└── lib/pages/
    └── environment_recommendation_page.dart  # Updated with PDF button
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GOOGLE_API_KEY` is set in your `.env` file
2. **Font Error**: Check if font files exist in `backend/ttf_files/`
3. **Permission Error**: Ensure storage permissions are granted on mobile devices
4. **Network Error**: Check internet connectivity for LLM API calls

### Debug Mode

Enable debug logging by setting `FLASK_ENV=development` in your `.env` file.

## Security Notes

- API keys should be kept secure and not committed to version control
- PDF files are temporarily stored and automatically cleaned up
- All API endpoints require authentication (JWT tokens)
