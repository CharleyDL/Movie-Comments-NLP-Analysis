import json
import mysql.connector


def get_db_config(filepath):
    f = open(filepath, "r")
    config = json.load(f)
    f.close
    return config


def db_connect(config):
    try:
        # recupération infos db
        db = mysql.connector.connect(**config)
        return db

    except Exception as e:
        print(e)

    # finally:
    #     if db.is_connected():
    #         print(db.get_server_info)
