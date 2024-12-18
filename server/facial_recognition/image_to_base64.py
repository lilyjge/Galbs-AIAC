'''
Converts target image to base64 and prints to output file.

Used to generate test data for server.
'''

import base64

image_path = 'facial_recognition/test_image_1.png'
output_path = 'facial_recognition/image_base64_output.txt'
with open(image_path, 'rb') as f:
    image_data = f.read()
    image_data_base64 = base64.b64encode(image_data)
    with open(output_path, 'w') as out:
        out.write(image_data_base64.decode('utf-8'))
        print('Image data converted to base64 and written to output.txt.')