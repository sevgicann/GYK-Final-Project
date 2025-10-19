import google.generativeai as genai
import os
from fpdf import FPDF
from dotenv import load_dotenv
import json
from typing import Dict, Any, List


environment_recommendation_prompt = '''
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

Our input variables: the crop is {crop_name}(user input), region is {region}(user input).
List and explain these variables in flowing paragraphs, not bullet points:
- Soil Type  = {soil_type} (model prediction result)
- Irrigation method  = {irrigation_method} (model prediction result)
- Fertilizer type  = {fertilizer_type} (model prediction result)
- Sunlight duration / intensity = {sunlight} (model prediction result)

---

### 2. Uygun Olmayan Koşulların Sonuçları (Negative Effects / Risks)

Explain what would happen if the environment is **too cold, too hot, too dry, too wet, too acidic, or too alkaline** for this specific crop in this specific region.  
Give detailed physiological or yield-related effects (e.g., "Yüksek sıcaklık domateste çiçek dökümüne neden olur.").

---

### Additional Instructions

- Keep the tone natural, explanatory, and farmer-friendly.  
- Write in connected paragraphs — no bullet points.  
- Mention the **reason (why)** behind every condition.  
- Always tie explanations to the **given crop and region**; never use generic agricultural statements.  
- Although this prompt is written in English, the output must be in Turkish.

'''


crop_recommendation_prompt = '''Important: The final report must be written in Turkish.

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

Fertilizer: {fertilizer_type} (user input)

pH: {ph} (user input)

Nitrogen (ppm): {nitrogen} (user input)

Phosphorus (ppm): {phosphorus} (user input)

Potassium (ppm): {potassium} (user input)

Humidity (%): {humidity} (user input)

Temperature (°C): {temperature} (user input)

Annual Rainfall (mm): {rainfall} (user input)

Model Prediction Results

{recommendations}

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


def clean_text(text: str):
    text = text.replace("*", "")
    text = text.replace("--", "")
    text = text.replace("#", "")
    return text


def write_string_to_pdf(text: str, filename: str = "crop_recommendation.pdf"):
    text = clean_text(text)
    
    pdf = FPDF()
    
    # Try to add custom fonts, fallback to default if not available
    try:
        pdf.add_font("Calibri", "", "ttf_files/calibri.ttf", uni=True)
        pdf.add_font("Calibri", "B", "ttf_files/calibrib.ttf", uni=True)
    except:
        print("Custom fonts not found, using default fonts")
    
    pdf.add_page()
    pdf.set_font("Calibri", size=12)
    
    paragraphs = text.strip().split('\n\n')
    
    for paragraph in paragraphs:
        if paragraph.strip():
            if ':' in paragraph and len(paragraph.split(':')[0]) < 50:
                title_part = paragraph.split(':')[0] + ':'
                content_part = paragraph.split(':', 1)[1].strip()
                
                pdf.set_font("Calibri", 'B', size=12)
                pdf.cell(w=0, h=8, txt=title_part, ln=1, align="L")
                
                pdf.set_font("Calibri", size=11)
                pdf.multi_cell(w=0, h=6, txt=content_part, align="J")
                pdf.ln(3)
            else:
                pdf.set_font("Calibri", size=11)
                pdf.multi_cell(w=0, h=6, txt=paragraph.strip(), align="J")
                pdf.ln(3)
    
    pdf.output(filename)
    print(f"PDF file successfully created: {filename}")


def generate_crop_recommendation_pdf(data: Dict[str, Any]) -> str:
    """Generate crop recommendation PDF and return the file path"""
    try:
        # Extract data from the input dictionary
        location = data.get('location', 'Bilinmeyen')
        region = data.get('region', 'Bilinmeyen')
        soil_type = data.get('soil_type', 'Bilinmeyen')
        sunlight = data.get('sunlight', 'Bilinmeyen')
        irrigation_method = data.get('irrigation_method', 'Bilinmeyen')
        fertilizer_type = data.get('fertilizer', 'Bilinmeyen')
        ph = data.get('ph', 6.5)
        nitrogen = data.get('nitrogen', 100)
        phosphorus = data.get('phosphorus', 50)
        potassium = data.get('potassium', 200)
        humidity = data.get('humidity', 25)
        temperature = data.get('temperature', 20)
        rainfall = data.get('rainfall', 500)
        recommendations = data.get('recommendations', [])
        
        # Get the main recommended crop
        crop_name = recommendations[0].get('product_name', 'Bilinmeyen Ürün') if recommendations else 'Bilinmeyen Ürün'
        
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Format recommendations for the prompt
        recommendations_text = ""
        for i, rec in enumerate(recommendations, 1):
            product_name = rec.get('product_name', f'Ürün {i}')
            confidence = rec.get('confidence', 0.0)
            suitability_percentage = int(confidence * 100)
            recommendations_text += f"{product_name} ({suitability_percentage}% suitability) (model prediction result)\n"
        
        # Format the prompt with actual data
        formatted_prompt = crop_recommendation_prompt.format(
            location=location,
            region=region,
            soil_type=soil_type,
            sunlight=sunlight,
            irrigation_method=irrigation_method,
            fertilizer_type=fertilizer_type,
            ph=ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            humidity=humidity,
            temperature=temperature,
            rainfall=rainfall,
            recommendations=recommendations_text.strip()
        )
        
        # Generate content using LLM
        response = model.generate_content(formatted_prompt)
        response_text = response.text
        
        # Generate unique filename
        import time
        timestamp = int(time.time())
        filename = f"crop_recommendation_{location}_{timestamp}.pdf"
        
        # Create PDF
        write_string_to_pdf(response_text, filename)
        
        return {
            'success': True,
            'message': f'PDF raporu başarıyla oluşturuldu: {filename}',
            'filename': filename,
            'content': response_text
        }
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return {
            'success': False,
            'message': f'PDF oluşturulurken hata oluştu: {str(e)}',
            'error': str(e)
        }


def generate_environment_conditions_pdf(
    crop_name: str,
    region: str,
    soil_type: str,
    irrigation_method: str,
    fertilizer_type: str,
    sunlight: str
) -> Dict[str, Any]:
    """
    Generate a PDF report for environment conditions using LLM
    """
    try:
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Format the prompt with actual data
        formatted_prompt = environment_recommendation_prompt.format(
            crop_name=crop_name,
            region=region,
            soil_type=soil_type,
            irrigation_method=irrigation_method,
            fertilizer_type=fertilizer_type,
            sunlight=sunlight
        )
        
        # Generate content using LLM
        response = model.generate_content(formatted_prompt)
        response_text = response.text
        
        # Generate unique filename
        import time
        timestamp = int(time.time())
        filename = f"environment_conditions_{crop_name}_{timestamp}.pdf"
        
        # Create PDF
        write_string_to_pdf(response_text, filename)
        
        # Return the file path instead of a dictionary
        return filename
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise e


if __name__ == "__main__":
    # Test the function
    test_recommendations = [
        {'product_name': 'Domates', 'confidence': 0.8},
        {'product_name': 'Mısır', 'confidence': 0.7},
        {'product_name': 'Pirinç', 'confidence': 0.6}
    ]
    
    result = generate_crop_recommendation_pdf(
        location="Ankara",
        region="İç Anadolu",
        soil_type="Tınlı Toprak",
        sunlight="Güneşli",
        irrigation_method="Damla Sulama",
        fertilizer_type="Organik Gübre",
        ph=6.5,
        nitrogen=120,
        phosphorus=60,
        potassium=225,
        humidity=26,
        temperature=23,
        rainfall=850,
        recommendations=test_recommendations
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))