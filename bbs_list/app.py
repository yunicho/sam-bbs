import json
import boto3
import pymysql
import math

def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="ap-northeast-2"
    )
    get_secret_value_response = client.get_secret_value(
        SecretId='lambda'
    )
    token = get_secret_value_response['SecretString']
    return eval(token)


def db_ops():
    secrets = get_secret()
    try:
        connection = pymysql.connect(
            host=secrets['host'],
            user=secrets['username'],
            password=secrets['password'],
            db='mydb',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    except pymysql.MySQLError as e:
        print("connection error!!")
        return e

    print("connection ok!!")
    return connection


def lambda_handler(event, context):
    conn = db_ops()
    cursor = conn.cursor()

    try:
        cursor.execute("select * from bbs")
        result = cursor.fetchall()
        body = json.dumps({
            "message": "success",
            "data":result
        })

        return {
            "statusCode": 200,
            # Cross Origin처리
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            "body": body,
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            # Cross Origin처리
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'
            },
            "body": json.dumps({
                "message": "fail",
            }),
        }