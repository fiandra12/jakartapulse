pipeline {
  agent any
  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }
  triggers { pollSCM('H/5 * * * *') }
  environment { IMAGE = 'jakartapulse-etl:latest' }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Prepare env') {
      steps {
        withCredentials([file(credentialsId: 'jakartapulse-env', variable: 'ENV_FILE')]) {
          sh 'cp "$ENV_FILE" .env'
        }
      }
    }

    stage('Build image') { steps { sh 'docker compose build etl-runner' } }

    stage('Lint') {
      steps { sh 'docker run --rm $IMAGE flake8 etl tests --max-line-length=120' }
    }

    stage('Unit test') {
      steps { sh 'docker run --rm $IMAGE pytest -q' }
    }

    stage('Deploy stack') {
      steps { sh 'docker compose up -d --build --wait postgres metabase' }
    }

    stage('Smoke run ETL') {
      steps { sh 'docker compose --profile etl run --rm etl-runner' }
    }
  }

  post {
    always  { sh 'rm -f .env' }
    success { echo 'CI/CD sukses' }
    failure { echo 'CI/CD gagal, cek log' }
  }
}
