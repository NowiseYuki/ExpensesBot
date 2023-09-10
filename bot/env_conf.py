from dotenv import dotenv_values

config_dict = {**dotenv_values('.env')}

BOT_TOKEN = config_dict["BOT_TOKEN"]
DB_PARAMS = {"dbname": config_dict["DB_NAME"],
             "user": config_dict["DB_USER"],
             "password": config_dict["DB_USER_PWD"],
             "host": config_dict["DB_HOST"],
             "port": config_dict["DB_PORT"]}
