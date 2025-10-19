import google.generativeai as genai
import os
from fpdf import FPDF
from dotenv import load_dotenv


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
- Mention cause–effect relations explicitly (“Sıcaklık 25°C’nin altına düştüğünde polen canlılığı azalır, bu da meyve tutumunu düşürür.”).

Our input variables: the crop is Oat, region is Marmara.
List and explain these variables in flowing paragraphs, not bullet points:
- Soil Type  = Kumlu Toprak
- Irrigation method  = Damla sulama
- Fertilizer type  = Amonyum Sülfat
- Sunlight duration / intensity = Güneşli

---

### 2. Uygun Olmayan Koşulların Sonuçları (Negative Effects / Risks)

Explain what would happen if the environment is **too cold, too hot, too dry, too wet, too acidic, or too alkaline** for this specific crop in this specific region.  
Give detailed physiological or yield-related effects (e.g., “Yüksek sıcaklık domateste çiçek dökümüne neden olur.”).

---

### Example Input

Crop: Domates  
Location: Amasya  
Region: Karadeniz Bölgesi  

---

### Example Output (in Turkish)

**Domates – Karadeniz Bölgesi İçin Gerekli Koşullar**

**Gerekli Çevresel Koşullar ve Bilimsel Gerekçeleri:**  
Toprak Tipi: Domates, iyi drene olan hafif kireçli veya kumlu-tınlı topraklarda gelişir. Çünkü bu yapı, köklerin hava almasını ve besin emilimini kolaylaştırır.  
pH: 6.0–6.8 aralığı idealdir; bu aralıkta demir ve çinko gibi mikro elementlerin alımı en verimli düzeydedir. Daha yüksek pH’da bu elementlerin alımı azalır.  
Sıcaklık: 22–28°C, çiçeklenme ve meyve tutumu için en uygun aralıktır; 18°C’nin altında polen canlılığı düşer, 35°C’nin üzerinde ise meyve dökümü artar.  
... [diğer değişkenler aynı biçimde açıklanır]

**Uygun Olmayan Koşulların Sonuçları:**  
Sıcaklık 30°C’nin üzerine çıktığında bitki stres hormonları artar, bu da çiçek dökümüne yol açar.  
Aşırı kireçli topraklarda demir eksikliği görülür, yapraklar sararır.  
Yetersiz güneş ışığı meyve rengini ve tadını olumsuz etkiler.  
... [benzeri şekilde devam eder]

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

Environmental Data

Location: Amasya

Region: Eastern Anatolia

Soil Type: Calcareous (lime-rich) soil

Sunlight: Partial shade

Irrigation Method: Sprinkler

Fertilizer: Compost

pH: 6.5

Nitrogen (ppm): 120

Phosphorus (ppm): 60

Potassium (ppm): 225

Humidity (%): 26

Temperature (°C): 23

Annual Rainfall (mm): 850

Model Prediction Results

Tomato (80% suitability)

Maize/Corn (70% suitability)

Rice (60% suitability)

Output Instructions

For each crop, follow the structure below. Write the report in Turkish.

Crop Name (Suitability Percentage)

Positive Effects (Advantages):
[Explain the conditions that favor this crop’s growth. Summarize the effect of each environmental variable in a single, coherent paragraph with smooth narration.]

Negative Effects / Risks (Disadvantages):
[Explain the conditions that may limit growth or pose risks. Describe the negative impact of each environmental variable in a single, clear paragraph.]

Additional Rules

Preserve scientific accuracy, while simplifying technical terms.

Explanations should be narrative paragraphs, not bullet lists.

Use a natural tone that a farmer can easily relate to their own field.

Each crop’s section should read like a self-contained mini report.

Clearly state cause–effect relationships when appropriate (e.g., “Lime in the soil supplies calcium for tomatoes, which helps reduce blossom drop.”).
!!! When giving explanations, write the variables on a new line after the colon. Each new variable should be on a separate line.
!! Only respond according to the conditions I give you and never make any other comments.

Reminder: Although this prompt is written in English, the generated report must be in Turkish.'''


def clean_text(text: str):
    text = text.replace("*", "")
    text = text.replace("--", "")
    text = text.replace("#", "")
    return text

def write_string_to_pdf(text: str):
    text = clean_text(text)
    
    pdf = FPDF()
    pdf.add_font("Calibri", "", "ttf_path/calibri.ttf", uni=True)
    try:
        pdf.add_font("Calibri", "B", "ttf_path/calibrib.ttf", uni=True)
    except:
        print("Bold font not found, using normal font")
    
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
    
    pdf.output("environment_conditions.pdf")
    print("PDF file successfully created")

def main():
    try:
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        ttf_path = os.getenv('FONT_PATH')


        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        genai.configure(api_key=api_key)
        # Select the model to use
        model = genai.GenerativeModel('gemini-2.5-flash')
    
        # Send your prompt
        
        response = model.generate_content(crop_recommendation_prompt)
    
        response_text = response.text
        print(type(response_text), response_text)
        write_string_to_pdf(response_text)

    
    except Exception as e:
        print(f"An error occurred: {e}")