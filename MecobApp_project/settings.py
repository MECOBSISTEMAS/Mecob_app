#Esse arquivo tem configurações principais para o App mecob

#
import os #biblioteca para manipular arquivos da maquina
from pathlib import Path #dependencia para manipular as rotas dos arquivos do projeto atual
import random #dependencia para geração de numeros e caracteres aleatorios
import string #conjunto de caracteres
#?importando o dotenv e carregando as variaveis de ambiente
import dotenv #importação e das variaveis de ambiente virtual do aruqivo .env
dotenv.load_dotenv()

gerador_de_caracteres = lambda quantidade: ''.join(random.choices(string.ascii_letters + string.digits, k=quantidade))

BASE_DIR = Path(__file__).resolve().parent.parent

#caso a variavel chamada SECRET_KEY não seja encontrada sera substituido por um valor aleatorio com 32 caracteres
SECRET_KEY = os.getenv('SECRET_KEY', gerador_de_caracteres(32))

DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']#!habiliatndo qualquer link para puxar dados, alterar depois


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #?apps
    'Core_app',
    #?dependencias
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'dj_rest_auth',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'MecobApp_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MecobApp_project.wsgi.application'

#Configuração para o banco de dados
if os.getenv('DB_ENGINE') and os.getenv('DB_ENGINE') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DATABASE'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT'),
        }
    }
else: #caso a variavel de ambiente chamada DB_ENGINE não seja encontrada o projeto sera inciado usando um arquivo SQLite como banco de dados
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

#Autenticação exigida ao se cadastrar no projeto, remoção para facilitar a criação do superusuario
AUTH_PASSWORD_VALIDATORS = [
]
""" {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }, """


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br' #configuração para a linguagem do projeto, caso achar necessario pode colocar de volta para o padrão: en-us

TIME_ZONE = 'America/Sao_Paulo' #configuração da timezone, horario em que o projeto esta configurado

USE_I18N = True  #tradução

USE_TZ = True #confirma a utilização da configuração do timezone


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/' #onde sera armazenado os arquivos estaticos
STATIC_ROOT = 'staticfiles/' #onde sera armazenado os arquivos estaticos em pordução

MEDIA_URL = '/media/' #onde sera armazenado os arquivos de media 
MEDIA_ROOT = 'media/' #onde sera armazenado os arquivos de media em produção

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    #? configuração da paginação por elementos
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'Core_app.api.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,  # Número de elementos por página
}

CORS_ORIGIN_ALLOW_ALL = True
#? Caso habilite como False, devera colocar a rota que é permitiddo o acesso
""" 
CORS_ORIGIN_WHITELIST = (
  'http://localhost:8000',
) 
"""

""" REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
} """


#Configuração para o envio de email caso o usario solicite o reset-password (enviar o token para o email)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

#?usar o envio de email no prompt do proprio django para teste
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

