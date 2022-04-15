# lambda-r53-ddns
Lambda と Route53 を使用して DDNS を実現する。


## Example
```
ENDPOINT="lambda エンドポイントURL" #h #ttps://hogehoge.lambda-url.ap-northeast-3.on.aws
REGION="Lambda のリージョン" # ap-notrheast-1
ZONE_ID="更新対象の Route53 Zone ID"
DOMAIN="更新対象のドメイン名" # hoge.example.com


url  -XPOST  ${ENDPOINT}  -H "Content-Type: application/json"  -d '{ "zone_id": "${ZONID}", "domain_name": "${DOMAIN}"}'    --aws-sigv4 "aws:amz:${REGION}:lambda"    --user "${AWS_ACCESS_KEY_ID}:${AWS_SECRET_ACCESS_KEY}" | jq
```
