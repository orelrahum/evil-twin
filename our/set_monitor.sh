#!/bin/bash


interface=$1

ifconfig $interface down
iwconfig $interface mode monitor
ifconfig $interface up

