from PIL import Image as PI
from wand.image import Image
import pyocr
import pyocr.builders
import io
import os
import sys


os.chdir(r'd:\Work_201712_PCM\20171225')

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

req_img=[]
img_pdf=Image(filename=r'd:\Work_201712_PCM\20171225\KKN8564.pdf',resolution=300)
image_jpeg=img_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    img_page=Image(image=img)
    req_img.append(img_page.make_blob('jpeg'))

for img in req_img:
    txt=tool.image_to_string(
        PI.open(io.BytesIO(img)),
        lang="eng",
        builder=pyocr.builders.TextBuilder()
        )
    print(txt)
    print("**************************************")


