# ajrlewis_app

![My Package Logo](static/img/logo.png)

## About

Public repository for the https://www.ajrlewis.com website.

## Installation

Clone the project

```bash
git clone https://github.com/ajrlewis/ajrlewis_app.git
cd ajrlewis_app
```

Install with the following script:

```bash
bash scripts/install.sh
```

## Running the App

Set the following `.env` variables:

| Variable | Description |
| :------- | :---------- |
| MAIL_SERVER | |
| MAIL_PORT | |
| MAIL_USERNAME | |
| MAIL_PASSWORD | |
| MAIL_DEFAULT_SENDER_NAME | |
| MAIL_USE_TLS | |
| MAIL_USE_SSL | |
| RECAPTCHA_PUBLIC_KEY | |
| RECAPTCHA_PRIVATE_KEY | |
| REMEMBER_COOKIE_DURATION | |
| DATABASE_USERNAME | |
| DATABASE_PASSWORD | |
| DATABASE_QUERY | |
| SQLALCHEMY_DATABASE_URI | |
| SQLALCHEMY_TRACK_MODIFICATIONS | |
| APP_NAME | |
| APP_NOSTR | |
| APP_URL | |
| WOS_USERNAME | |
| WOS_USERNAME_ALIAS | |

And run locally using:

```bash
bash scripts/wsgi.sh 127.0.0.1 5000
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
