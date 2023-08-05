# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: 

    Author:           @diego.yosiura
    Last Update:      21/07/2021 19:53
    Created:          21/07/2021 19:53
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco_exclusivo_package
    IDE:              PyCharm
"""
from enum import Enum


class DiasModelos(Enum):
    WRF = 3
    COSMO = 5
    UKMO = 5
    ICON = 6
    ECMWF = 9
    GEM = 9
    ACCESSG = 9
    ETA = 10
    AMPERE = 10
    PREVC = 10
    NPREVC = 14
    ECMWFENS = 14
    GEFS = 15
    GFS = 15
    ECMWF46 = 45
    MEMBROS_00 = 180
    MEMBROS_06 = 180
    MEMBROS_12 = 180
    MEMBROS_18 = 180
    TROPICAL = 180
    INFORMES = 180
    ZERO = 180
    CLIMATOLOGIA = 180
    MERGE = 180