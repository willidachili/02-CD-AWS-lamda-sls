# Github Actions with Lambda, API Gateway and AWS SAM

Demo av using Github actions to deploy a Lambda in a Serverless application. I denne laben skal vi bruke 
AWS tjenesten "Comprehend" for å finne ut av om "stemningen" (Sentiment) i en tekst er negativt eller positivt 
ladet. Dette kan for eksempel brukes til å finne ut av om et produkt får god eller dårlig omtale i medier osv. 

## Log på Cloud 9 miljøet ditt 

## Lag en fork

Du må lage en fork av dette repositoryet inn i din egent GitHub konto

## Klone din fork inn i Cloud 9 miljøet ditt

## Endre på koden for å unngå navnekonflikter

## Test lokalt

I cloud 9 

```shell
cd <katalognanvn>
sam invoke local -e event.json 
```

Ta en ekstra kikk på event.json. Dette er objektet AWS Lambda får av tjenesten API Gateway 

## Deploy med SAM fra Cloid 9

Du kan også bruke SAM til å deploye lambdafunksjonen rett fra Cloud9 miljøet 

```shell
sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment-<bruker> --s3-bucket lambda-deployments-gb --capabilities CAPABILITY_IAM --region us-east-1
```

Men, dette er jo ikke veldig "DevOps" og vil ikke fungere i et større team. Vi trenger både CI og CD for å kunne jobbe 
effektivt sammen om denne funksjonen.

## GitHub Actions

Kopier  denne koden inn i  ```.github/workflows/``` katalogen, og kall den for eksempel sam-deploy.yml eller noe tilsvarende 

```yaml
on:
  push:
    branches:
      - main

defaults:
  run:
    working-directory: ./sentiment-demo

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - uses: aws-actions/setup-sam@v1
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - run: sam build --use-container
      - run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment --s3-bucket lambda-deployments-gb --capabilities CAPABILITY_IAM --region us-east-1
```

