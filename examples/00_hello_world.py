import pandas as pd
import base64
import matplotlib.pyplot as plt
def plotimg(df):
    df = df.astype(float)
    print(df) # It won't show anything in the cloud, but it does when run locally.

    plt.figure(figsize=(6.4, 4.8), dpi=100) # 640 x 480 pixels
    plt.plot(df)

    plt.savefig('/tmp/img.jpg', format='jpg')
    plt.close()

    return "/tmp/img.jpg"

def returnimg(ff):
    with open(ff, 'rb') as image_file:
        img = image_file.read()

    body = base64.b64encode(img).decode('utf-8')

    response = {
        'headers': {"Content-Type": "image/png"},
        'statusCode': 200,
        'body': body,
        'isBase64Encoded': True
    }
    return response

def handler(dfs):
    if len(dfs) > 0:
        df = dfs[0]
    else: # If dfs = [] let's set some dummy graph   
        df = pd.DataFrame({'timestamp': [0,1], 'value': [1,2]}).set_index('timestamp')

    ff = plotimg(df)

    response = returnimg(ff)

    return response


#################################################################
### Code to run locally, mimicking the cloud environment
DATASET_NAMES = ['qq']
OUTPUT_TYPE = 'jpg'

if 'TWO_MINLOG_EXECUTION_ENV' not in globals():
    import os
    import tempfile
    import pandas as pd
    import base64

    os.makedirs("/tmp", exist_ok=True)
    globals()['MPLCONFIGDIR'] = tempfile.mkdtemp(dir='/tmp')

    csvs = []
    for DSN in DATASET_NAMES:
        with open( DSN + '.csv', 'r') as f:
            data = f.readlines()
            data = [line.strip().split(',') for line in data]
            csvs.append(data)

    dfs = []
    for csv in csvs:
        if csv == [[]]:
            continue

        df = pd.DataFrame(data=csv[1:], columns=csv[0])
        df.set_index('timestamp', inplace=True)
        df.index = pd.to_datetime(df.index, format='ISO8601')
        dfs.append(df)

    result = handler(dfs)

    if OUTPUT_TYPE == 'png' or OUTPUT_TYPE == 'jpg':
        img_data = base64.b64decode(result['body'])

        with open('output.' + OUTPUT_TYPE, 'wb') as file:
            file.write(img_data)
    else:
        print(80*'*')
        print(result['body'])
        print(80*'*')


### Code to run locally, mimicking the cloud environment
#################################################################
