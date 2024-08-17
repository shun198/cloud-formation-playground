import logging
import os

import boto3

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ecs_client = boto3.client('ecs')
    elbv2_client = boto3.client('elbv2')

    # 環境変数から必要な情報を取得
    ecs_cluster_name = os.environ['ECS_CLUSTER_NAME']
    ecs_service_name = os.environ['ECS_SERVICE_NAME']
    target_group_arn = os.environ['TARGET_GROUP_ARN']

    try:
        if event['detail']['lastStatus'] == 'RUNNING':
            # ECS サービスの実行中タスクをリストアップ
            task_arns = ecs_client.list_tasks(
                cluster = ecs_cluster_name,
                serviceName = ecs_service_name,
                desiredStatus = 'RUNNING'
            ).get('taskArns')

            # 実行中タスクがない場合はエラーログを出力
            if not task_arns:
                message = 'No running tasks found for the service.'
                logger.error(message)
                return {'message': message}

            # 実行中タスクの詳細情報を取得
            task_details = ecs_client.describe_tasks(
                cluster = ecs_cluster_name,
                tasks = task_arns
            )

            # 実行中タスクからプライベート IP アドレスを取得
            targets = [
                {'Id': detail['value']}
                for task in task_details['tasks']
                for attachment in task['attachments']
                if attachment['type'] == 'ElasticNetworkInterface'
                for detail in attachment['details']
                if detail['name'] == 'privateIPv4Address'
            ]

            # プライベート IP アドレスが見つからない場合はエラーログを出力
            if not targets:
                message = 'No private IP addresses found for the tasks.'
                logger.error(message)
                return {'message': message}

            # ALBのターゲットグループに対象の IP アドレスを登録
            elbv2_client.register_targets(
                TargetGroupArn = target_group_arn,
                Targets = targets
            )

            # 登録したターゲットのログ出力
            logger.info(f'Registered targets: {[target["Id"] for target in targets]}')

            # 登録が成功した場合、対象の IP アドレスとターゲットグループ ARN を返す
            return {
                'message': 'Successfully registered targets.',
                'registered_targets': [target['Id'] for target in targets],
                'target_group_arn': target_group_arn
            }

        elif event['detail']['lastStatus'] == 'STOPPED':
            # ECS サービスの実行中タスクをリストアップ
            task_arns = ecs_client.list_tasks(
                cluster = ecs_cluster_name,
                serviceName = ecs_service_name,
                desiredStatus = 'RUNNING'
            ).get('taskArns')

        # 実行中タスクがない場合はエラーログを出力
        if not task_arns:
            message = 'No running tasks found for the service.'
            logger.error(message)
            return {'message': message}

        # 実行中タスクの詳細情報を取得
        task_details = ecs_client.describe_tasks(
            cluster = ecs_cluster_name,
            tasks = task_arns
        )

        # 実行中タスクからプライベート IP アドレスを取得
        ecs_ip_addresses = [
            detail['value']
            for task in task_details['tasks']
            for attachment in task['attachments']
            if attachment['type'] == 'ElasticNetworkInterface'
            for detail in attachment['details']
            if detail['name'] == 'privateIPv4Address'
        ]

        # プライベート IP アドレスが見つからない場合はエラーログを出力
        if not ecs_ip_addresses:
            message = 'No private IP addresses found for the tasks.'
            logger.error(message)
            return {'message': message}

        # ALB に登録済みのターゲットを取得する (Unhealthy も含む)
        alb_target_health = elbv2_client.describe_target_health(
            TargetGroupArn = target_group_arn
        )['TargetHealthDescriptions']

        # 登録済みターゲットの IP アドレスを取り出し、リストに追加する
        alb_ip_addresses = []
        for t in alb_target_health:
            alb_ip_addresses.append(t['Target']['Id'])

        # 実行中タスクの IP アドレスと登録済みターゲットの IP アドレスを比較する
        deregister_targets = []
        for alb_ip_address in alb_ip_addresses:
            if alb_ip_address not in ecs_ip_addresses:
                deregister_targets.append({"Id": alb_ip_address})

        # 対象の IP アドレスがある場合、ターゲットグループから削除する
        elbv2_client.deregister_targets(
            TargetGroupArn = target_group_arn,
            Targets = deregister_targets
        )
        # 削除したターゲットのログ出力
        logger.info(f'Deregistered targets: {[target["Id"] for target in deregister_targets]}')

        # 削除が成功した場合、対象の IP アドレスとターゲットグループ ARN を返す
        return {
            'message': 'Successfully deregistered targets.',
            'deregistered_targets': [target['Id'] for target in deregister_targets],
            'target_group_arn': target_group_arn
        }

    except Exception as e:
        # 例外が発生した場合、エラーメッセージをログに記録し、レスポンスとして返す
        logger.error(f'Error registering targets: {str(e)}')
        return {'message': f'Error: {str(e)}'}
