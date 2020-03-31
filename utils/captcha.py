import base64
import io

import captcha.image


def get_captcha_base64(content, b64=False):
    image = captcha.image.ImageCaptcha().generate_image(content)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    if not b64:
        return buffered.getvalue()
    return base64.b64encode(buffered.getvalue())
