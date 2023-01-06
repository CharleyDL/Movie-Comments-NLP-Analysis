#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 5 Jan. 2023
# ==============================================================================

from flask import Flask

from config_flask import Config


app = Flask(__name__) # crée une instance de Flask 
app.jinja_env.auto_reload = True
app.config.from_object(Config)


from app import route