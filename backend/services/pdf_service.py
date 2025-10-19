import os
import tempfile
from typing import Dict, Any, Optional
from flask import current_app
from utils.logger import get_logger
import google.generativeai as genai
from fpdf import FPDF
from dotenv import load_dotenv

logger = get_logger('services.pdf_service')

class PDFService:
    """Service for generating PDF reports using LLM and FPDF"""
    
    def __init__(self):
        self._load_environment_variables()
        self._configure_gemini()
    
    def _load_environment_variables(self):
        """Load required environment variables"""
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.font_path = os.getenv('FONT_PATH', 'backend/ttf_files')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        logger.info("PDF Service environment variables loaded successfully")
    
    def _configure_gemini(self):
        """Configure Google Generative AI"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Gemini AI configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini AI: {str(e)}")
            raise
    
    def generate_environment_recommendation_pdf(self, 
                                              crop: str, 
                                              location: str, 
                                              region: str,
                                              soil_type: str,
                                              irrigation_method: str,
                                              fertilizer_type: str,
                                              sunlight: str) -> Dict[str, Any]:
        """
        Generate PDF report for environment recommendations
        
        Args:
            crop: The crop name
            location: The location/city
            region: The region
            soil_type: Type of soil
            irrigation_method: Irrigation method used
            fertilizer_type: Type of fertilizer
            sunlight: Sunlight conditions
            
        Returns:
            Dict containing success status, file path, and metadata
        """
        try:
            logger.info(f"Generating environment recommendation PDF for {crop} in {location}")
            
            # Create the prompt
            prompt = self._create_environment_recommendation_prompt(
                crop, location, region, soil_type, irrigation_method, fertilizer_type, sunlight
            )
            
            # Generate content using LLM
            response = self.model.generate_content(prompt)
            content = response.text
            
            logger.info("LLM content generated successfully")
            
            # Create PDF
            pdf_path = self._create_pdf_from_content(content, f"environment_conditions_{crop.lower()}.pdf")
            
            return {
                'success': True,
                'file_path': pdf_path,
                'content': content,
                'metadata': {
                    'crop': crop,
                    'location': location,
                    'region': region,
                    'generated_at': self._get_current_timestamp()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating environment recommendation PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'PDF oluşturulurken hata oluştu'
            }
    
    def generate_crop_recommendation_pdf(self, 
                                       location: str,
                                       region: str,
                                       soil_type: str,
                                       sunlight: str,
                                       irrigation_method: str,
                                       fertilizer: str,
                                       ph: float,
                                       nitrogen: float,
                                       phosphorus: float,
                                       potassium: float,
                                       humidity: float,
                                       temperature: float,
                                       rainfall: float,
                                       top_3_predictions: list) -> Dict[str, Any]:
        """
        Generate PDF report for crop recommendations
        
        Args:
            location: The location/city
            region: The region
            soil_type: Type of soil
            sunlight: Sunlight conditions
            irrigation_method: Irrigation method
            fertilizer: Fertilizer type
            ph: Soil pH
            nitrogen: Nitrogen content
            phosphorus: Phosphorus content
            potassium: Potassium content
            humidity: Humidity percentage
            temperature: Temperature in Celsius
            rainfall: Rainfall in mm
            top_3_predictions: List of top 3 crop predictions with suitability scores
            
        Returns:
            Dict containing success status, file path, and metadata
        """
        try:
            logger.info(f"Generating crop recommendation PDF for {location}, {region}")
            
            # Create the prompt
            prompt = self._create_crop_recommendation_prompt(
                location, region, soil_type, sunlight, irrigation_method, fertilizer,
                ph, nitrogen, phosphorus, potassium, humidity, temperature, rainfall,
                top_3_predictions
            )
            
            # Generate content using LLM
            response = self.model.generate_content(prompt)
            content = response.text
            
            logger.info("LLM content generated successfully")
            
            # Create PDF
            pdf_path = self._create_pdf_from_content(content, f"crop_recommendation_{location.lower()}.pdf")
            
            return {
                'success': True,
                'file_path': pdf_path,
                'content': content,
                'metadata': {
                    'location': location,
                    'region': region,
                    'generated_at': self._get_current_timestamp()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating crop recommendation PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'PDF oluşturulurken hata oluştu'
            }
    
    def _create_environment_recommendation_prompt(self, crop, location, region, soil_type, 
                                                irrigation_method, fertilizer_type, sunlight):
        """Create the prompt for environment recommendations"""
        return f'''
Important: The final report must be written in Turkish.

You are an AI agricultural specialist experienced in plant physiology, climate adaptation, and soil science.

Your task is to prepare a detailed and explanatory report describing **why** each environmental and soil condition is necessary for the healthy growth of the given crop in the specified region.

The goal is not to give generic advice, but to explain:
- Why the crop needs certain temperature, moisture, pH, or soil conditions.
- How the regional climate affects these needs.
- What happens (positively or negatively) if these conditions deviate from the ideal range.

Structure the report in two parts:

---

### 1. Gerekli Çevresel Koşullar ve Bilimsel Gerekçeleri (Ideal / Recommended Conditions and Their Reasons)

For each environmental variable, explain in Turkish:
- Why this factor is important for the given crop.  
- The ideal range or type (e.g., "Domates için 6.0–6.8 pH aralığı, köklerin besin alımını optimize eder çünkü...").  
- How this condition interacts with the regional climate or soil type.  
- Mention cause–effect relations explicitly ("Sıcaklık 25°C'nin altına düştüğünde polen canlılığı azalır, bu da meyve tutumunu düşürür.").

Our input variables: the crop is {crop} (user input), region is {region} (user input).
List and explain these variables in flowing paragraphs, not bullet points:
- Soil Type = {soil_type} (model prediction result)
- Irrigation method = {irrigation_method} (model prediction result)
- Fertilizer type = {fertilizer_type} (model prediction result)
- Sunlight duration / intensity = {sunlight} (model prediction result)

---

### 2. Uygun Olmayan Koşulların Sonuçları (Negative Effects / Risks)

Explain what would happen if the environment is **too cold, too hot, too dry, too wet, too acidic, or too alkaline** for this specific crop in this specific region.  
Give detailed physiological or yield-related effects (e.g., "Yüksek sıcaklık domateste çiçek dökümüne neden olur.").

---

### Example Input

Crop: {crop}  
Location: {location}  
Region: {region}

---

### Additional Instructions

- Keep the tone natural, explanatory, and farmer-friendly.  
- Write in connected paragraphs — no bullet points.  
- Mention the **reason (why)** behind every condition.  
- Always tie explanations to the **given crop and region**; never use generic agricultural statements.  
- Although this prompt is written in English, the output must be in Turkish.
'''
    
    def _create_crop_recommendation_prompt(self, location, region, soil_type, sunlight, 
                                         irrigation_method, fertilizer, ph, nitrogen, 
                                         phosphorus, potassium, humidity, temperature, 
                                         rainfall, top_3_predictions):
        """Create the prompt for crop recommendations"""
        
        # Format top 3 predictions
        predictions_text = ""
        for i, (crop_name, suitability) in enumerate(top_3_predictions[:3], 1):
            predictions_text += f"\n{crop_name} ({int(suitability * 100)}% suitability) (model prediction result)"
        
        return f'''Important: The final report must be written in Turkish.

You are an AI expert in agricultural production, plant physiology, and soil science.
Based on the environmental conditions and soil data provided below, prepare a detailed and explanatory evaluation report for three crops suggested by the model.

For each crop, analyze how the given conditions affect its growth, development, and yield potential.
Structure your assessment under two headings:

Positive Effects (Advantages)

Negative Effects / Risks (Disadvantages)

Under each heading, address all environmental variables (soil type, pH, moisture, temperature, sunlight, fertilizer, irrigation, rainfall, etc.) one by one; however, explain them within a single, flowing paragraph, using clear, farmer-friendly language that links the factors together.
Maintain scientific accuracy; simplify agricultural terms with brief explanations when necessary.

Environmental Data (user input)

Location: {location} (user input)

Region: {region} (user input)

Soil Type: {soil_type} (user input)

Sunlight: {sunlight} (user input)

Irrigation Method: {irrigation_method} (user input)

Fertilizer: {fertilizer} (user input)

pH: {ph} (user input)

Nitrogen (ppm): {nitrogen} (user input)

Phosphorus (ppm): {phosphorus} (user input)

Potassium (ppm): {potassium} (user input)

Humidity (%): {humidity} (user input)

Temperature (°C): {temperature} (user input)

Annual Rainfall (mm): {rainfall} (user input)

Model Prediction Results

{predictions_text}

Output Instructions

For each crop, follow the structure below. Write the report in Turkish.

Crop Name (Suitability Percentage)

Positive Effects (Advantages):
[Explain the conditions that favor this crop's growth. Summarize the effect of each environmental variable in a single, coherent paragraph with smooth narration.]

Negative Effects / Risks (Disadvantages):
[Explain the conditions that may limit growth or pose risks. Describe the negative impact of each environmental variable in a single, clear paragraph.]

Additional Rules

Preserve scientific accuracy, while simplifying technical terms.

Explanations should be narrative paragraphs, not bullet lists.

Use a natural tone that a farmer can easily relate to their own field.

Each crop's section should read like a self-contained mini report.

Clearly state cause–effect relationships when appropriate (e.g., "Lime in the soil supplies calcium for tomatoes, which helps reduce blossom drop.").
!!! When giving explanations, write the variables on a new line after the colon. Each new variable should be on a separate line.
!! Only respond according to the conditions I give you and never make any other comments.

Reminder: Although this prompt is written in English, the generated report must be in Turkish.'''
    
    def _create_pdf_from_content(self, content: str, filename: str) -> str:
        """Create PDF file from content using FPDF"""
        try:
            # Clean the content
            cleaned_content = self._clean_text(content)
            
            # Create PDF
            pdf = FPDF()
            
            # Add fonts
            try:
                pdf.add_font("Calibri", "", f"{self.font_path}/calibri.ttf", uni=True)
                pdf.add_font("Calibri", "B", f"{self.font_path}/calibrib.ttf", uni=True)
            except Exception as e:
                logger.warning(f"Could not load custom fonts, using default: {str(e)}")
                # Use default fonts if custom fonts are not available
                pdf.set_font("Arial", size=12)
            
            pdf.add_page()
            pdf.set_font("Calibri", size=12)
            
            # Split content into paragraphs
            paragraphs = cleaned_content.strip().split('\n\n')
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Check if paragraph contains a title (has colon and short first part)
                    if ':' in paragraph and len(paragraph.split(':')[0]) < 50:
                        title_part = paragraph.split(':')[0] + ':'
                        content_part = paragraph.split(':', 1)[1].strip()
                        
                        # Add title
                        try:
                            pdf.set_font("Calibri", 'B', size=12)
                        except:
                            pdf.set_font("Arial", 'B', size=12)
                        pdf.cell(w=0, h=8, txt=title_part, ln=1, align="L")
                        
                        # Add content
                        try:
                            pdf.set_font("Calibri", size=11)
                        except:
                            pdf.set_font("Arial", size=11)
                        pdf.multi_cell(w=0, h=6, txt=content_part, align="J")
                        pdf.ln(3)
                    else:
                        # Regular paragraph
                        try:
                            pdf.set_font("Calibri", size=11)
                        except:
                            pdf.set_font("Arial", size=11)
                        pdf.multi_cell(w=0, h=6, txt=paragraph.strip(), align="J")
                        pdf.ln(3)
            
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, filename)
            
            # Output PDF
            pdf.output(pdf_path)
            
            logger.info(f"PDF created successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error creating PDF: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing markdown formatting"""
        text = text.replace("*", "")
        text = text.replace("--", "")
        text = text.replace("#", "")
        return text
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def cleanup_pdf_file(self, file_path: str) -> bool:
        """Clean up temporary PDF file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up PDF file: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error cleaning up PDF file: {str(e)}")
        return False

# Global instance
_pdf_service = None

def get_pdf_service() -> PDFService:
    """Get or create PDF service instance"""
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFService()
    return _pdf_service
