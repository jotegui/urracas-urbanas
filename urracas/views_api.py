# -*- coding: utf-8 -*-

import os
import hashlib
from flask import render_template, redirect, url_for, request, flash, session, g
from . import app, db
from . import functions as f


### ZONA API

