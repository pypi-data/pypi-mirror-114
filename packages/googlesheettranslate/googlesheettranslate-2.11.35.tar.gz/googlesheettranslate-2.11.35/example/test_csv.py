# !/usr/bin/env python
# coding: utf-8
import os

from googlesheettranslate.main import GoogleTranslationSheet

ROOT = os.path.join(os.path.dirname(__file__))

builder = GoogleTranslationSheet().builderOutputTarget(ROOT).builderFromCSV("tr_csv.csv")

# builder.GetReader().overrideFileFormat("_{}.json", True)
builder.builderTransformers("Android")
builder.run("CN")
builder.run("EN")
builder.run("RU")

builder.builderTransformers("i18n")
builder.run("RU")
builder.run("FR")
builder.run("EN")
