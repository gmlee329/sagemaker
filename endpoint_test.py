def infer(input_image):
    from boto3.session import Session
    import json
    from PIL import Image
    import io
    # from requests_toolbelt.multipart.encoder import MultipartEncoder
    import numpy as np
    import time
    import im_utils

    def img_to_npy(img):
        img = im_utils.check_angle(img)
        img = im_utils.make_square(img)
        img = img.convert('RGB')
        img = im_utils.resize_img(img, shape=(100,100))
        img = np.array(img).reshape(1,100,100,3) / 255.
        return img

    img = Image.open(input_image)
    img = img_to_npy(img)

    img = img.tolist()
    test_data = {
        'img' : img
    }
    payload = json.dumps(test_data)

    s = time.time()
    session = Session()

    runtime = session.client("runtime.sagemaker")

    response = runtime.invoke_endpoint(
        EndpointName='larva-model',
        ContentType='application/json',
        Body=payload)

    result = json.loads(response["Body"].read())
    print(type(result))
    print (result, time.time()-s)
    result = json.dumps(result, ensure_ascii=False)
    print(type(result))
    result = json.loads(result)
    print(type(result))

infer('./sample_img/bed.png')