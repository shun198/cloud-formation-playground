# 概要

AWS CloudFormation でインフラをコード化する際は

- テンプレート
- スタック

を使って作業をします

## テンプレート

json または yml 形式のファイルのことです<br>
AWS のリソースを構築する際はテンプレートを使用します<br>
以下の公式サイトのテンプレートスニペットを参考にすれば作成できます<br>

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/CHAP_TemplateQuickRef.html

```yml
AWSTemplateFormatVersion: 2010-09-09
Description: A sample template
Resources:
  MyEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: ami-0ff8a91507f77f867
      InstanceType: t2.micro
      KeyName: testkey
      BlockDeviceMappings:
        - DeviceName: /dev/sdm
          Ebs:
            VolumeType: io1
            Iops: 200
            DeleteOnTermination: false
            VolumeSize: 20
```

## スタック

テンプレートによって作成された環境群のことを指します

# リソース

以下のリソースを使用できます

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html

# パラメータ

パラメーターを使用すると、スタックを作成または更新するたびにテンプレートにカスタム値を入力できます

```yml
Parameters:
  InstanceTypeParameter:
    Type: String
    Default: t2.micro
    AllowedValues:
      - t2.micro
      - m1.small
      - m1.large
    Description: Enter t2.micro, m1.small, or m1.large. Default is t2.micro.
```

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html

## SSM パラメータタイプ

```yml
Parameters:
  InstanceType:
    Type: 'AWS::SSM::Parameter::Value<String>'
Resources:
  Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: !Ref InstanceType
```

# Mapping

key と value のセットで値をマッピングできる
以下が使用例

```yml
AWSTemplateFormatVersion: '2010-09-09'
Mappings:
  RegionMap:
    us-east-1:
      HVM64: ami-0ff8a91507f77f867
      HVMG2: ami-0a584ac55a7631c0c
    us-west-1:
      HVM64: ami-0bdb828fd58c52235
      HVMG2: ami-066ee5fd4a9ef77f1
    eu-west-1:
      HVM64: ami-047bb4163c506cd98
      HVMG2: ami-0a7c483d527806435
    ap-northeast-1:
      HVM64: ami-06cd52961ce9f0d85
      HVMG2: ami-053cdd503598e4a9d
    ap-southeast-1:
      HVM64: ami-08569b978cc4dfa10
      HVMG2: ami-0be9df32ae9f92309
Resources:
  myEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', HVM64]
      InstanceType: m1.small
```

## パラメータプロパティ

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#parameters-section-structure-properties

## 擬似パラメータ

| パラメータ名          | 説明                                                                         |
| --------------------- | ---------------------------------------------------------------------------- |
| AWS::AccountId        | スタックが作成されているアカウントの AWS アカウント ID を返します            |
| AWS::NotificationARNs | ARN のリストを返します                                                       |
| AWS::NoValue          | 組み込み関数の戻り値として指定すると、対応するリソースプロパティを削除します |
| AWS::Partition        | リソースがあるパーティションを返します                                       |
| AWS::Region           | リージョン名を返します                                                       |
| AWS::StackId          | スタック ID を返します                                                       |
| AWS::StackName        | スタック名を返します                                                         |
| AWS::URLSuffix        | ドメインのサフィックスを返します                                             |

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html

# ルール関数

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-rules.html

# 出力

```yml
Outputs:
  BackupLoadBalancerDNSName:
    Description: The DNSName of the backup load balancer
    Value: !GetAtt BackupLoadBalancer.DNSName
    Condition: CreateProdResources
  InstanceID:
    Description: The Instance ID
    Value: !Ref EC2Instance
```

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html

# EC2 UserData

```yml
UserData:
  Fn::Base64: !Sub |
    #!/bin/bash -xe
    yum update -y aws-cfn-bootstrap
    /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfig --region ${AWS::Region}
    /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerGroup --region ${AWS::Region}
```

# Metadata

# 組み込み関数

AWS CloudFormation には、スタックの管理に役立ついくつかの組み込み関数が用意されています

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html

## Ref

指定したパラメータまたはリソースの値を返します

```yml
MyEIP:
  Type: 'AWS::EC2::EIP'
  Properties:
    InstanceId: !Ref MyEC2Instance
```

## FindInMap

```yml
Mappings:
  RegionMap:
    us-east-1:
      HVM64: 'ami-0ff8a91507f77f867'
      HVMG2: 'ami-0a584ac55a7631c0c'
    us-west-1:
      HVM64: 'ami-0bdb828fd58c52235'
      HVMG2: 'ami-066ee5fd4a9ef77f1'
    eu-west-1:
      HVM64: 'ami-047bb4163c506cd98'
      HVMG2: 'ami-31c2f645'
    ap-southeast-1:
      HVM64: 'ami-08569b978cc4dfa10'
      HVMG2: 'ami-0be9df32ae9f92309'
    ap-northeast-1:
      HVM64: 'ami-06cd52961ce9f0d85'
      HVMG2: 'ami-053cdd503598e4a9d'
Resources:
  myEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !FindInMap
        - RegionMap
        - !Ref 'AWS::Region'
        - HVM64
      InstanceType: m1.small
```

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-findinmap.html

## Sub

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html
