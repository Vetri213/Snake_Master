import HandTrackingModule as htm

detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

def pose(img):
    img = detector.findHands(img)
    first_lmList = detector.findPosition(img, draw=False)
    second_lmList = detector.findPosition(img, draw=False, handNo = 1)
    pose = [None,None]
    if len(first_lmList) != 0:
        if first_lmList[8][2] > first_lmList[7][2] and first_lmList[8][2] > first_lmList[6][2] and first_lmList[8][2] > first_lmList[5][2] and first_lmList[8][2] > first_lmList[9][2] and first_lmList[8][2] > first_lmList[13][2]:
            pose[0] = "down"
        elif first_lmList[8][2] < first_lmList[7][2] and first_lmList[8][2] < first_lmList[6][2] and first_lmList[8][2] < first_lmList[5][2] and first_lmList[8][2] < first_lmList[9][2] and first_lmList[8][2] < first_lmList[13][2] and first_lmList[10][2] < first_lmList[3][2]:
            pose[0] = "up"
        elif first_lmList[8][1] < first_lmList[10][1] and first_lmList[8][1] < first_lmList[7][1] and first_lmList[8][1] < first_lmList[6][1] and first_lmList[8][1] < first_lmList[5][1]:
            pose[0] = "right"
        elif first_lmList[8][1] > first_lmList[2][1] and first_lmList[8][1] > first_lmList[7][1] and first_lmList[8][1] > first_lmList[6][1] and first_lmList[8][1] > first_lmList[5][1]:
            pose[0] = "left"

    if len(second_lmList) != 0:
        fingers = []
        # Thumb
        if second_lmList[tipIds[0]][1] < second_lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #Fingers
        for id in range(1, 5):
            if second_lmList[tipIds[id]][2] < second_lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        if fingers.count(1) ==4:
            pose[1] = "quit"
        elif fingers.count(1) == 3:
            pose[1] = "continue"
        elif fingers.count(1) == 2:
            if fingers[1] and fingers[4]:
                pose[1] = "exit"

    return pose

    """
        up_down = "normal"
        right_left = "none"
        total_flipped = 0
        total_right = 0
        total_left = 0
        for i in range(1, 5):
            if first_lmList[tipIds[i]][2] > first_lmList[0][2]:
                total_flipped += 1

        if total_flipped > 3:
            up_down = "flipped"

        for i in range(1, 5):
            if first_lmList[tipIds[i]][1] < first_lmList[0][1]:
                total_right +=1
            if first_lmList[tipIds[i]][1] > first_lmList[0][1]:
                total_left +=1
        if total_left > 3:
            right_left = "left"
        elif total_right > 3:
            right_left = "right"


        if up_down == "normal":
            #Thumb
            if first_lmList[tipIds[0]][1] > first_lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):
                if first_lmList[tipIds[id]][2] < first_lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            #print (fingers)
            totalFingers = fingers.count(1)
            #print (totalFingers)
        else:
            # Thumb
            if first_lmList[tipIds[0]][1] > first_lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if first_lmList[tipIds[id]][2] > first_lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            totalFingers = fingers.count(1)
            # print (totalFingers)
        #print(fingers)
        pose = ""
        if totalFingers == 1 and fingers[1]:
            if right_left == "none":
                if up_down == "normal":
                    pose = "up"
                else:
                    pose = "down"
            elif right_left == "right":
                pose = "right"
            elif right_left == "left":
                pose = "left"
        """
