# Github Actions with Lambda, API Gateway and AWS SAM

Demo av Github actions, og hvordan vi kan sette opp en CD pipeline for en AWS Lambdafunksjon. I denne laben skal vi bruke 
AWS tjenesten "Comprehend" for å finne ut av om "stemningen" (Sentiment) i en tekst er negativt eller positivt 
ladet. Dette kan for eksempel brukes til å finne ut av om et produkt får god eller dårlig omtale i medier osv. 

Vi skal også se på hvoordan vi kan bruke Feature toggles med Unleash for å slå av/på funkskjonalitet dynamisk 
uten å gjøre nye deployments. 

Vi skal også se på verktøyet "AWS SAM" for å 

## Lag en fork

Du må lage en fork av dette repositoryet til din egen GitHub konto.

![Alt text](img/fork.png  "a title")

## Logg i Cloud 9 miljøet ditt 

![Alt text](img/aws_login.png  "a title")

* Logg på med din AWS bruker med URL, brukernavn og passord gitt i klassrommet
* Gå til tjenesten Cloud9 (Du nå søke på Cloud9 uten mellomrom i søket) 
* Velg "Open IDE" 
* Hvis du ikke ser ditt miljø, kan det hende du har valgt feil region. Hvilken region du skal bruke vil bli oppgitt i klasserommet.

### Lag et Access Token for GitHub

Når du skal autentisere deg mot din GitHub konto fra Cloud 9 trenger du et access token.  Gå til  https://github.com/settings/tokens og lag et nytt.

![Alt text](img/generate.png  "a title")

Access token må ha "repo" tillatelser, og "workflow" tillatelser.

![Alt text](img/new_token.png  "a title")

### Lage en klone av din Fork (av dette repoet) inn i ditt Cloud 9 miljø

For å slippe å autentisere seg hele tiden kan man få git til å cache nøkler i et valgfritt
antall sekunder på denne måten;

```shell
git config --global credential.helper "cache --timeout=86400"
```

OBS Når du gjør ```git push``` senere og du skal autentisere deg, skal du bruke GitHub Access token når du blir bedt om passord, 
så du trenger å ta vare på dette et sted. 

Klone repository med HTTPS URL

![Alt text](img/clone.png  "a title")

```
git clone https://github.com/≤github bruker>/02-CD-AWS-lamda-sls
```

## Endre på koden for å unngå navnekonflikter

Siden alle studentene deler en AWS konto, er det viktig at alle ressurser som lages    
I template.yml - se etter koden 

```shell
  Prefix:
    Description: Change this to avoid naming conflicts 
    Type: String
    Default: glennbech
```

Her skal du bytte ut verdien "glennbech" med ditt eget navn, eller noe du tror vil være unikt blant de andre deltagerene i samme lab. 

## Test deployment fra Cloud 9

I cloud 9, åpne en Terminal

```shell
cd <katalognanvn>
sam build --use-container
sam invoke local -e event.json 
```

* Ta en ekstra kikk på event.json. Dette er objektet AWS Lambda får av tjenesten API Gateway .
* Du kan gjerne forsøke å endre teksten i event.json for å få en posirive review

## Deploy med SAM fra Cloid 9

Du kan også bruke SAM til å deploye lambdafunksjonen rett fra Cloud9 miljøet 

```shell
sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment-<bruker> --s3-bucket lambda-deployments-gb --capabilities CAPABILITY_IAM --region us-east-1
```

Du kan deretter bruke for eksempel postman eller Curl til å teste ut tjenesten 

```shell
curl -X POST \
  <din URL her> \
  -H 'Content-Type: text/plain' \
  -H 'cache-control: no-cache' \
  -d 'The laptop would not boot up when I got it. It would let me get through a few steps of the setup process, then it would become unresponsive and eventually shut down, then restar, '
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

## Bonus-utfordring 

Se om dere kan bruke andre 