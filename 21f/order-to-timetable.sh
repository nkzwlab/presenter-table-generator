#!/usr/bin/env bash

awk -f csv.awk $1 | python3 table.py
