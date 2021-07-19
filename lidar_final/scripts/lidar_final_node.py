#!/usr/bin/env

from genpy import message
import rospy
from sensor_msgs.msg import LaserScan
from lidar_final.msg import lidar_final_msgs
import math

min_mesafe = 2


def inf_remover(mesafe):
    return [item for item in mesafe if item!=math.inf]

def inf_counter(mesafe):
    count = 0
    for x in range(len(mesafe)):
        if math.isinf(mesafe[x]) == True:
            count += 1
    return count

def on_engel_tespiti(on_mesafe):
    if inf_counter(on_mesafe) < 70:
        return True #Eger deger True ise engel var!
    return False

def sol_mesafe_tespiti(sol_mesafe):
    float = 0
    sol_mesafe_final = sol_mesafe
    if math.inf in sol_mesafe:
        sol_mesafe_final = inf_remover(sol_mesafe)

    for x in sol_mesafe_final:
        float += x

    if float != 0:
        float = float / len(sol_mesafe_final)
        if float != None:
            return float


def sag_mesafe_tespiti(sag_mesafe):
    float = 0
    sag_mesafe_final = sag_mesafe
    if math.inf in sag_mesafe:
        sag_mesafe_final = inf_remover(sag_mesafe)

    for x in sag_mesafe_final:
        float += x

    if float != 0:
        float = float / len(sag_mesafe_final)
        if float != None:
            return float
    

def callback(data):
    mesafe = list(data.ranges)

    on_mesafe = mesafe[140:220]
    orta_aci = on_mesafe[40]
    sag_mesafe = mesafe[:5]
    sol_mesafe = mesafe[355:]

    msg = lidar_final_msgs()

    if sag_mesafe_tespiti(sag_mesafe) != None:
        msg.sag = sag_mesafe_tespiti(sag_mesafe)
    if sol_mesafe_tespiti(sol_mesafe) != None:
        msg.sol = sol_mesafe_tespiti(sol_mesafe)
    msg.on = orta_aci
    msg.durum = on_engel_tespiti(on_mesafe)

    pub.publish(msg)

if __name__ == '__main__':
    try:
        rospy.init_node('lidar_final_node', anonymous=True)
        sub = rospy.Subscriber('/scan_filtered', LaserScan, callback)
        pub = rospy.Publisher('/lidar_final_msg', lidar_final_msgs, queue_size=10)
        rate = rospy.Rate(1)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
