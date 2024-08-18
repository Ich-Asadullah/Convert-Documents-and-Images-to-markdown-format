import asyncio
import fitz
from io import BytesIO
import base64
import os
import httpx
from PIL import Image

async def encode_image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

async def send_image_to_chat(image_base_64):

    headers = {"x-api-key" : os.environ.get("ANTROPIC_API_KEY"),
       "anthropic-version": "2023-06-01",
     "content-type": "application/json"}
    
    data = {
          "model" : "claude-3-5-sonnet-20240620",
          "max_tokens" : 4096,
          "messages" : [
              {"role": "user", "content": [
              {
                "type": "image",
                "source": {
                  "type": "base64",
                  "media_type": "image/png",
                  "data": image_base_64,
                }
              },
              {"type": "text", "text": "Return whole content of this image in markdown format. If you are unable to find any text in image, just return 'N/A'."}
            ]}
          ]
        }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        result = response
        return result.json()

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
        pdf_bytes = pdf_file.read()
        images = pdf_to_images(pdf_bytes)
        markdown_results = []
        total_cost = 0
        total_inp_tokens = 0
        total_res_tokens = 0

        async def process_image(image):
            img_base64 = await encode_image_to_base64(image)
            response = await send_image_to_chat(img_base64)
            text_content = response['content'][0]['text']
            # Estimate tokens
            inp_tokens = response['usage']['input_tokens']
            output_tokens = response['usage']['output_tokens']

            return text_content, inp_tokens, output_tokens

        tasks = [process_image(image) for image in images]
        results = await asyncio.gather(*tasks)

        for result, inp_tokens, res_tokens in results:
            markdown_results.append(result)
            total_inp_tokens += inp_tokens
            total_res_tokens += res_tokens

        total_cost = estimate_cost(total_inp_tokens, total_res_tokens)

        return markdown_results, total_cost, total_inp_tokens, total_res_tokens

async def process_image(image_file):
        image_bytes = image_file.read()
        image = await asyncio.get_event_loop().run_in_executor(None, lambda: Image.open(BytesIO(image_bytes)))
        img_base64 = await encode_image_to_base64(image)
        response = await send_image_to_chat(img_base64)
        # print(response)
        text_content = response['content'][0]['text']
        # Estimate tokens
        inp_tokens = response['usage']['input_tokens']
        output_tokens = response['usage']['output_tokens']

        total_cost = estimate_cost(inp_tokens, output_tokens)
        return text_content, total_cost, inp_tokens, output_tokens

def estimate_cost(input_tokens, output_tokens):
    return ((3/1000000)*input_tokens) + ((15/1000000)*output_tokens)