def handleKeyboard(p):
    keys = p.getKeyboardEvents()
    for k, v in keys.items():
        # print(k)
        
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x = maxAcc*sim.dt
            goingRight = True
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x = -maxAcc*sim.dt
            # x = 0
        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_x = -maxAcc*sim.dt
            goingRight = False
        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_x = maxAcc*sim.dt

        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y = -maxAcc*sim.dt
            goingFront = True
        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y = maxAcc*sim.dt
            
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            deltaMax_y = maxAcc*sim.dt
            goingFront = False            
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED)):
            deltaMax_y = -maxAcc*sim.dt
    
