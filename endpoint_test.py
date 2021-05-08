def infer(input_image):
    from boto3.session import Session
    import json
    from PIL import Image
    import io
    # from requests_toolbelt.multipart.encoder import MultipartEncoder
    import numpy as np
    import time

    img = Image.open(input_image)
    # img = open(input_image, 'rb').read()
    # output = io.BytesIO()
    # img.save(output, format="png")
    # image_as_string = output.getvalue()
    # test_data = {
    #     'img' : [1, 2, 3.0],
    # }
    # payload = json.dumps(test_data)

    # payload = MultipartEncoder(
    #     fields={
    #         'img': image_as_string,
    #     })

    img = img.resize(size=(80,80))
    img = np.array(img)
    img = img.reshape(1,80,80,3) / 255.
    img = img.tolist()
    test_data = {
        'img' : img
    }
    payload = json.dumps(test_data)

    s = time.time()
    session = Session()

    runtime = session.client("runtime.sagemaker")

    response = runtime.invoke_endpoint(
        EndpointName='resnet',
        ContentType='application/json',
        Body=payload)

    result = json.loads(response["Body"].read())
    print (result, time.time()-s)
    result = json.dumps(result, ensure_ascii=False)
    print(result)
infer('./sample_img/bed.png')