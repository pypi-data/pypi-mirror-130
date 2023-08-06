#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright (C) 2021 David Arroyo Menéndez

#  Author: David Arroyo Menéndez <davidam@gmail.com> 
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com> 
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
# 
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with Damegender; see the file GPL.txt.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
#  Boston, MA 02110-1301 USA,


import csv

diccmales = {}
diccfemales = {}

with open('scotland.orig.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(reader, None)

    for row in reader:
        if (row[1] == 'B'):
            if row[2] in diccmales.keys():
                diccmales[row[2]] = diccmales[row[2]] + int(row[3])
            else:
                diccmales[row[2]] = int(row[3])
        elif (row[1] == 'G'):
            if row[2] in diccfemales.keys():
                diccfemales[row[2]] = int(diccfemales[row[2]]) + int(row[3])
            else:
                diccfemales[row[2]] = int(row[3])

fomales = open("scotland.males.borns.csv", "w")

for i in diccmales.keys():
    fomales.write(i + "," + str(diccmales[i]) + "\n")

fomales.close()

fofemales = open("scotland.females.borns.csv", "w")

for i in diccfemales.keys():
    fofemales.write(i + "," + str(diccfemales[i]) + "\n")

fofemales.close()
