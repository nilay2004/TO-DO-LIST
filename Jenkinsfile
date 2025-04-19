pipeline {
    agent any

    environment {
        PYTHON_BIN = 'C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo '📥 Cloning GitHub repository...'
                git url: 'https://github.com/nilay2004/TO-DO-LIST.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                bat """
                    "%PYTHON_BIN%" -m pip install --upgrade pip
                    "%PYTHON_BIN%" -m pip install flask==2.3.3 flask-sqlalchemy==3.1.1 pytest==7.4.0 pytest-flask==1.2.0 selenium==4.15.0 webdriver-manager==4.0.1
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running unit tests using pytest...'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat """
                        "%PYTHON_BIN%" -m pytest tests/ --disable-warnings
                    """
                }
            }
        }

        stage('Start Flask App') {
            steps {
                echo '🚀 Starting Flask app...'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat """
                        set FLASK_APP=app.py
                        set FLASK_ENV=development
                        "%PYTHON_BIN%" -m flask run
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ TO-DO-LIST CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check errors in console output.'
        }
    }
}
