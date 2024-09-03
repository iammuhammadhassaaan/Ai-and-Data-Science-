from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import requests
import base64
from io import BytesIO

app = Flask(__name__)

# Hugging Face API URL (replace with actual API endpoint if using a paid plan)
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN"  # Replace with your Hugging Face API token

def generate_image(prompt, size, tone):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"size": size, "tone": tone}}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for failed requests
    return Image.open(BytesIO(response.content))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        size = request.form['size']
        tone = request.form['tone']
        # Generate image from prompt
        image = generate_image(prompt, size, tone)
        
        # Save the image to a BytesIO object
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Encode image data to base64
        image_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # Store prompt and settings
        with open('prompts.txt', 'a') as file:
            file.write(f"Prompt: {prompt}, Size: {size}, Tone: {tone}\n")

        return render_template('index.html', image_data=image_data, prompt=prompt, size=size, tone=tone)

    return render_template('index.html')

@app.route('/download')
def download_image():
    img_data = request.args.get('image_data')
    img_byte_arr = io.BytesIO(base64.b64decode(img_data))
    image = Image.open(img_byte_arr)
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

if __name__ == '__main__':
    app.run(debug=True)
