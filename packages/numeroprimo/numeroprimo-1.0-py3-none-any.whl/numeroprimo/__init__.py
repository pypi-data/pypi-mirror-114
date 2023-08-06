#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: ramon
"""
def sumaEnteros(a,b):
	return(a+b)

def restaEnteros(a,b):
	return(a-b)
	
def multiplicaEnteros(a,b):
	return(a*b)

def factorial(a):
	resultado = 1
	for i in range(1,a+1):
		resultado *= i
	
	return(resultado)
