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

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html

## パラメータプロパティ

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#parameters-section-structure-properties

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

https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html
