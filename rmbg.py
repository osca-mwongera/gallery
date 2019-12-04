import requests

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    data={
        'image_file': '/home/osca/Documents/ClassWork/gallery/photo/2019/1203/IMAG4805.jpg',
        'size': 'auto'
    },
    headers={'X-Api-Key': 'jwVycxCPbofMG4FDLTjdRZpD'},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
