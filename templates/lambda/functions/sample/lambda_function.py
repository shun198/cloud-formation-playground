def lambda_handler(event, context) -> str:
    """Lambdaのエントリーポイント
    """
    print(event["Records"][0]["body"])
    return "finish lambda"
