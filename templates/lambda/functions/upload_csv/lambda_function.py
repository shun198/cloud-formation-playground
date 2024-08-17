#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""実行スクリプト
"""

import json
import os
import urllib.parse

import requests


def lambda_handler(event, context) -> str:
    """Lambdaのエントリーポイント
    Args:
        event (_type_): lambdaが呼び出し時に与えられる値、大抵はJSON
        context (_type_): _description_

    Returns:
        str: lambdaの実行結果文字列
    """

    print("lambda_handler")
    body = json.loads(event["Records"][0]["body"])
    lambda_token = getParameterStoreValue(os.environ.get("LAMBDA_TOKEN"))
    url = getParameterStoreValue(os.environ.get("INTERNAL_BACK_SRV_URL")) + f"/api/customers/register_csv"
    data = {"token": lambda_token}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=json.dumps(data).encode(), headers=headers)
    print(response.status_code)
    print(response.json()["msg"])

    return "finish lambda"


def getParameterStoreValue(parameter_path: str):
    """パラメータストアに設定されている値を取得する
    パラメータストアのパスを指定して、対応する設定値を取得する
    前提:
        - NATゲートウェイを用いたインターネット通信が可能
        - AWS-Parameters-and-Secrets-Lambda-Extension レイヤーが存在する
    参考:
        - https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/ps-integration-lambda-extensions.html
    Args:
        parameter_path (str): SSMパラメータストアのパス
    Returns:
        _type_: パラメータストアに登録されている値
    """

    # 初期値は2773
    port = "2773"
    encoded_parameter_path = urllib.parse.quote_plus(parameter_path)
    parameter_store_url = (
        "http://localhost:"
        + port
        + "/systemsmanager/parameters/get/?name="
        + encoded_parameter_path
        + "&withDecryption=true"
    )

    # SSM:ParameterStoreにはヘッダーが必要なため追加
    # AWS-Parameters-and-Secrets-Lambda-Extensionレイヤーが前提
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    headers = {"X-Aws-Parameters-Secrets-Token": aws_session_token}
    r = requests.get(parameter_store_url, headers=headers)
    return json.loads(r.text)["Parameter"]["Value"]


# コマンドライン呼び出しの場合のみ、明示的にlambda_handler関数を呼び出す（local環境テストのため）
if __name__ == "__main__":
    lambda_handler("", "")
