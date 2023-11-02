class MissionariesState:
    """
    This class is used to represent a state of the missionaries
    and cannibals problem. Each state contains the number of
    missionaries and cannibals in each shore, the position
    of the boat, and the capacity of the boat to determine
    whether a state is valid or not.
    """

    def __init__(self, left_miss, left_cann, right_miss, right_cann, boat_position, capacity=2):
        self.miss = (left_miss, right_miss)  # missionaries in left and right shores
        self.cann = (left_cann, right_cann)  # cannibals in left and right shores
        self.boat_position = boat_position  # boat position ('left', 'right')
        self.capacity = capacity  # boat capacity (missionaries+cannibals)

    def __str__(self):
        to_str = "(%d, %d)" % (self.miss[0], self.cann[0])
        if self.boat_position == "left":
            to_str += " (||)      "
        else:
            to_str += "      (||) "
        to_str += "(%d, %d)" % (self.miss[1], self.cann[1])
        return to_str

    def __eq__(self, other):
        return self.miss == other.miss and self.cann == other.cann and self.boat_position == other.boat_position

    def succ(self, action):
        capacity = self.capacity
        cann_izq = self.cann[0]
        cann_drch = self.cann[1]
        miss_izq = self.miss[0]
        miss_drch = self.miss[1]
        misioneros_accion = int(action[1])
        canibales_accion = int(action[2])

        if (misioneros_accion + canibales_accion) > 0:      
            if action[0] == '>':
                if (self.miss[0] < misioneros_accion) or (self.cann[0] < canibales_accion):            
                    return None 

                miss_izq -= misioneros_accion
                miss_drch += misioneros_accion
                cann_izq -=  canibales_accion
                cann_drch += canibales_accion
                boat_pos = 'right'
                   
            if action[0] == '<':
                if (self.miss[1] < misioneros_accion) or (self.cann[1] < canibales_accion):
                    return None

                miss_izq += misioneros_accion
                miss_drch -= misioneros_accion
                cann_izq += canibales_accion
                cann_drch -= canibales_accion
                boat_pos = 'left'
                
            if (miss_drch == 0 or miss_drch >= cann_drch) and (miss_izq == 0 or miss_izq >= cann_izq):
                return MissionariesState(miss_izq, cann_izq, miss_drch, cann_drch, boat_pos, capacity)
            return None
        return None    

    #Algoritmo de Piedad
    def next_states(self):
        new_states= [] 
        M = 0
        C = 0
        action = ''

        if self.boat_position == 'left':
            action = '>'
        else:
            action = '<'

        while M <= self.capacity:
            while (M + C <= self.capacity) and (M >= C or M == 0):
                    action += str(M)
                    action +=str(C)
                    state = self.succ(action)
                    if state is not None:
                        new_states.append((state, action))
                    C += 1
                    action = action[0]
            C = 0
            M += 1        
        return new_states
