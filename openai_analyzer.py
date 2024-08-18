import asyncio
from openai import AsyncOpenAI
import fitz
from io import BytesIO
import base64
import os
from PIL import Image

async def encode_image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

async def send_image_to_chat(client, image_base64):
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Please process the image and return the content in Markdown format. If you are unable to find any text in image, just return 'N/A'."},
            {"role": "user", "content":[
            {
              "type": "text",
              "text": "Read this image and return all the text in this image, in markdown format."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
              }
            }
          ]}
        ]
    )
    return response

def pdf_to_images(pdf_bytes):
    images = []
    document = fitz.open("pdf", pdf_bytes)
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

async def process_pdf(pdf_file):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    pdf_bytes = pdf_file.read()
    images = pdf_to_images(pdf_bytes)
    markdown_results = []
    total_cost = 0
    total_inp_tokens = 0
    total_res_tokens = 0

    async def process_image(image):
        img_base64 = await encode_image_to_base64(image)
        response = await send_image_to_chat(client, img_base64)
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

    tasks = [process_image(image) for image in images]
    results = await asyncio.gather(*tasks)

    for result, inp_tokens, res_tokens in results:
        markdown_results.append(result)
        total_inp_tokens += inp_tokens
        total_res_tokens += res_tokens

    total_cost = estimate_cost(total_inp_tokens, 5/1000000) + estimate_cost(total_res_tokens, 15/1000000)

    return markdown_results, total_cost, total_inp_tokens, total_res_tokens

async def process_image(image_file):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    image_bytes = image_file.read()
    image = await asyncio.get_event_loop().run_in_executor(None, lambda: Image.open(BytesIO(image_bytes)))
    img_base64 = await encode_image_to_base64(image)
    response = await send_image_to_chat(client, img_base64)
    result = response.choices[0].message.content
    inp_tokens = response.usage.prompt_tokens
    res_tokens = response.usage.completion_tokens
    total_cost = estimate_cost(inp_tokens, 0.15/1000000) + estimate_cost(res_tokens, 0.60/1000000)
    return result, total_cost, inp_tokens, res_tokens

def estimate_cost(total_tokens, cost_per_token):
    return total_tokens * cost_per_token