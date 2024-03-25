import json
import urllib.parse
import boto3
import pandas as pd
import io

print('Loading function')

s3 = boto3.client('s3')



def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    codecommit = boto3.client('codecommit')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response["Body"].read()
        read_excel_data = io.BytesIO(file_content)
        df = pd.read_excel(read_excel_data)
        print(df)
        dd = df.to_dict()

        
        res = []
        for key in dd.keys() :
            res.append(dd[key])
        fus = res[0]
        kis = []
        for key in fus.keys() :
            kis.append(fus[key])
        tus = res[1]
        gis = []
        for key in tus.keys() :
            gis.append(tus[key])
        para_values = {}
        for parameters, values in zip(kis,gis):
            para_values[parameters] = values
        print(para_values)
        Configuration = {"Parameters" : para_values, "StackPolicy" : {"Statement" : [{"Effect" : "Allow","NotAction" : "Update:Delete","Principal": "*","Resource" : "*"}]} }
        print(Configuration)
        output_bucket = 'lambda-trigger12'
        output_key = 'Parameters/Configuration.json'
        json_bytes = json.dumps(Configuration).encode('UTF-8')
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=json_bytes)
        return {
        'statusCode': 200,
        'body': 'JSON data uploaded successfully to S3!'
            }
        
            
        
        
        
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        
    
              
