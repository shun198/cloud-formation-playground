# @see https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/CloudFormation/MacrosExamples/PyPlate/python.yaml

import json
import traceback


def obj_iterate(obj, params):
    if isinstance(obj, dict):
        # 辞書の各キーと値に対して再帰的に処理を行う
        for k, v in obj.items():
            obj[k] = obj_iterate(v, params)
    elif isinstance(obj, list):
        # リスト内の各要素に対して再帰的に処理を行う
        for i, v in enumerate(obj):
            obj[i] = obj_iterate(v, params)
    elif isinstance(obj, str) and obj.startswith("#!PyPlate"):
        # 特定の条件を満たす文字列を処理
        params['output'] = None
        exec(obj, params)
        obj = params['output']
    return obj

def lambda_handler(event, context):
    # 受け取ったイベント情報を出力
    print(json.dumps(event))
    macro_response = {
        "requestId": event["requestId"],
        "status": "success"
    }
    try:
        params = {
            "params": event["templateParameterValues"],
            "template": event["fragment"],
            "account_id": event["accountId"],
            "region": event["region"]
        }
        # 入力のテンプレートを処理して更新
        macro_response["fragment"] = obj_iterate(event["fragment"], params)
    except Exception as e:
        # エラーが発生した場合、エラーメッセージを記録
        traceback.print_exc()
        macro_response["status"] = "failure"
        macro_response["errorMessage"] = str(e)
    return macro_response
