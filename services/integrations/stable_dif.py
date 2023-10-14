import base64
from typing import Any

import aiohttp
import requests

from settings import settings
from services import ImageStyles, IMAGES_STYLES_REPLICATE

from services.base.base import BaseService


NEGATIVE = '''text, watermark, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck''' # noqa


class StableDiffusionService(BaseService):
    host = settings.STABLE_API
    endpoint = "/sdapi/v1/txt2img"
    headers = {}

    def __pre_init__(self, **kwargs) -> None:
        self._prompt = kwargs.get('prompt')

    def _build_request_json(self) -> dict:
        data = {
            "json":
                {
                    "prompt": self._prompt,
                    "seed": -1,
                    "sampler_name": "Euler a",
                    "batch_size": 1,
                    "steps": 25,
                    "cfg_scale": 7,
                    "width": 512,
                    "height": 512,
                    "negative_prompt": NEGATIVE,
                    "denoising_strength": 0.75
                }
        }
        return data

    def _parse_response_json(self, response_json: dict) -> Any:
        b64_str = response_json['images'][0]
        return b64_str


class StabilityAIService(BaseService):
    host = settings.STABILITY_AI_API
    endpoint = "/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": "Bearer " + settings.STABILITY_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __pre_init__(self, **kwargs) -> None:
        self._prompt = kwargs.get('prompt')
        self._style = kwargs.get('style')
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        self.seed = kwargs.get('seed')

    def _build_request_json(self) -> dict:
        data = {
            "json":
                {
                    "text_prompts": [
                        {
                            "text": self._prompt,
                            "weight": 1.0,
                        },
                        {
                            "text": NEGATIVE,
                            "weight": -1.0,
                        },
                    ],
                    "cfg_scale": 7,
                    "clip_guidance_preset": "FAST_BLUE",
                    "height": 1024 if not self.height else self.height,
                    "width": 1024 if not self.width else self.width,
                    "samples": 1,
                    "seed": 0 if not self.seed else self.seed,
                    "steps": 30,
                    "style_preset": ImageStyles.CINEMATIC.value if not self._style else self._style,
                }
        }
        print(data)
        return data

    def _parse_response_json(self, response_json: dict) -> Any:
        b64_str: str = response_json['artifacts'][0]['base64']
        fake_image_url = ''
        # return base64.b64decode(b64_str), fake_image_url
        return b64_str, fake_image_url


class StabilityAIUpscale(StabilityAIService):
    endpoint = "/v1/generation/esrgan-v1-x2plus/image-to-image/upscale"
    headers = {
        "Authorization": "Bearer " + settings.STABILITY_API_KEY,
        # "Content-Type": "multipart/form-data",
        "Accept": "application/json",
    }

    def __pre_init__(self, **kwargs) -> None:
        self._image = kwargs.get('image')
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')

    def _build_request_json(self) -> dict:
        import io
        self._file = io.BytesIO(self._image)
        data = {
            "data": {
                "image": self._file,
            }
        }
        if self.height:
            data['data']['height'] = str(self.height)
        elif self.width:
            data['data']['width'] = str(self.width)
        return data

    def _parse_response_json(self, response) -> Any:
        fake_image_url = ''
        self._file.close()
        # return base64.b64decode(response['artifacts'][-1]['base64']), fake_image_url
        return response['artifacts'][-1]['base64'], fake_image_url


class ReplicateStableDiffusionService(BaseService):
    host = settings.REPLICATE_API
    endpoint = "v1/predictions"
    headers = {
        "Authorization": "Token " + settings.REPLICATE_API_TOKEN,
    }

    def __pre_init__(self, **kwargs) -> None:
        self._prompt = kwargs.get('prompt')
        self._style = kwargs.get('style')
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        self.seed = kwargs.get('seed')

    def _build_prompt(self) -> str:
        if not self._style:
            return IMAGES_STYLES_REPLICATE[ImageStyles.CINEMATIC.value]['prompt'].format(self._prompt)
        return IMAGES_STYLES_REPLICATE[self._style]['prompt'].format(prompt=self._prompt)

    def _build_negative_prompt(self) -> str:
        if not self._style:
            return IMAGES_STYLES_REPLICATE[ImageStyles.CINEMATIC.value]['negative_prompt'] + ", " + NEGATIVE
        return IMAGES_STYLES_REPLICATE[self._style]['negative_prompt'] + ", " + NEGATIVE

    def _build_request_json(self) -> dict:
        data = {
            "json":
                {
                    "version": "8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
                    "input": {
                        "prompt": self._build_prompt(),
                        "negative_prompt": self._build_negative_prompt(),
                        "height": 1024 if not self.height else self.height,
                        "width": 1024 if not self.width else self.width,
                        "seed": 0 if not self.seed else self.seed,
                        "steps": 30,
                        "scheduler": "K_EULER_ANCESTRAL"
                    }
                }
        }
        print(data)
        return data

    async def _parse_response(self) -> Any:
        if self.response.ok:
            return await self._parse_response_json(await self.response.json())
        else:
            text = await self.response.text()
            raise requests.exceptions.HTTPError(text)

    async def _parse_response_json(self, response_json: dict) -> Any:
        url = response_json['urls']['get']
        self.request_class.url = url
        self.request_class.method = 'GET'
        self.request_class.kwargs = {}
        return await self.get_output_url()

    async def get_output_url(self):
        while True:
            response = await self.request_class.make_request()
            if response.ok:
                response_json = await response.json()
                status = response_json['status']
                if status == 'failed':
                    print(response_json['error'])
                    return None, None
                output_content = response_json.get('output')
                if output_content:
                    self.output_url = output_content[0]
                    break
                else:
                    continue
        return await self.get_image()

    async def get_image(self):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    "GET", self.output_url,
                    headers=self.headers) as resp:
                content = await resp.read()
        return base64.b64encode(content).decode(), self.output_url
