# 環境構築
## cloudformation実行甩インスタンス
- Amazon Linux AMI 2014.09.1 (HVM) - ami-4985b048

```bash
sudo yum update
sudo yum install git jq
sudo pip install jmespath-terminal

curl -kL https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python
sudo pip install virtualenv virtualenvwrapper
sudo pip install autoenv

vi ~/.bashrc
# User specific aliases and functions
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source `which virtualenvwrapper.sh`
source `which activate.sh`

git clone git@github.com:twingo-b/cloudformation_troposphere.git
cd cloudformation_troposphere
pip install -r requirements.txt
```

## NATインスタンスのAMI確認

```bash
export AWS_DEFAULT_REGION='ap-northeast-1'
aws ec2 describe-images --owners amazon > describe-images.json
# jmespath-terminal でquery作成
jpterm describe-images.json

aws ec2 describe-images --owners amazon --query 'Images[?starts_with(to_string(Name),`amzn-ami-vpc-nat-hvm`) == `true`].{Name:Name,ImageId:ImageId}' | jq .
[
  {
    "Name": "amzn-ami-vpc-nat-hvm-2014.09.1.x86_64-gp2",
    "ImageId": "ami-27d6e626"
  },
  {
    "Name": "amzn-ami-vpc-nat-hvm-2014.03.2.x86_64-gp2",
    "ImageId": "ami-49c29e48"
  },
  {
    "Name": "amzn-ami-vpc-nat-hvm-2014.03.2.x86_64-ebs",
    "ImageId": "ami-55c29e54"
  }
]
```

## NATインスタンスのkey作成

```bash
aws ec2 create-key-pair --key-name gameday
```

# CloudFormation起動と停止
## 起動

```bash
python gen-vpc-with-public-and-private-subnets.py > $HOME/gen-vpc-with-public-and-private-subnets.json
export AWS_DEFAULT_REGION='ap-northeast-1'
aws cloudformation create-stack --stack-name gameday --template-body file:////home//ec2-user//gen-vpc-with-public-and-private-subnets.json
{
    "StackId": "arn:aws:cloudformation:ap-northeast-1:<account_num>:stack/gameday/9e210a00-7ddc-11e4-a549-5088487c4896"
}
```

## 停止
```bash
aws cloudformation delete-stack --stack-name gameday
```

# TODO
- cf2py検証

# 参考
## troposphere
 - https://github.com/bwhaley/aws-gameday-2014
 - https://github.com/cloudtools/troposphere
 - https://github.com/cloudtools/awacs

## pip,virtualenv,autoenv
 - http://qiita.com/who_you_me/items/831d62f396e6d66dda66
 - http://www.slideshare.net/who_you_me/10-32435124
 - http://www.kormoc.com/2014/03/22/autoenv-and-virtualenv/

## aws-cli
 - http://www.slideshare.net/AmazonWebServicesJapan/aws-black-belt-tech-aws-command-line-interface

