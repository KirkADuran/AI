#!/usr/bin/env python3
import math
import random
class node:
    """
    Node storing: End Position, End Velocity, Controls
    """
    def __init__(self, parent, x,y,dx,dy,O,s):
        self.parent = parent
        self.pos = [x, y]
        self.vel = [dx,dy]
        self.control = [O,s]

    def __eq__(self,other):
        return self.pos == other.pos


class World:
    def __init__(self,row,col,maze,sC,sR,gC,gR):
        """
        Class Requires: Row, Col, Maze strings, start and goal. Uses a list for node storage
        
        """
        self.counter = 0
        self.visited = []
        self.solved = False
        self.row = row
        self.col = col
        self.maze = maze
        self.sC = sC
        self.sR = sR
        self.gC = gC
        self.gR = gR
        self.current = node(None,sR,sC,0,0,None,None)
        self.visited.insert(0,self.current)


    def randomPosition(self):
        """
        Generates Random position: 5% chance to return goal. Returns [row, col]
        """
        e = random.uniform(0,100)
        if e >= 95:
            rR = self.gR
            rC = self.gC
        else:
            rR = random.uniform(0,self.row-1)
            rC = random.uniform(0,self.col-1)
        return [rR,rC]
        
    def isInObstacle(self,pos):
        """
        Checks to see if cell is occupied
        """
        row = int(pos[0])
        col = int(pos[1])

        if self.maze[row][col] =="#":
            return True
        else:
            return False

    def path(self):
        """
        Prints out list of controls
        """
        path = []
        state = self.visited[-1]
        path.append(state.control)
        parent = state.parent
        while(parent.parent is not None):
            state = parent
            parent = state.parent
            path.insert(0,state.control)
        print(len(path))
        for n in path:
            print(n[0], " ", n[1])


    def isThruObstacle(self,old,new):
        """
        Given a candidate random node and a node from the graph. Generates a random angle and magnitude. 
        Projects in time and checks for collisions at each time step.
        Returns the trajectory that gets closest
        """
        newS = None
        newO = None

        closest = float("inf")
        R1,C1 = old.pos[0],old.pos[1]
        R2,C2 = new[0],new[1]
        dR,dC = old.vel[0],old.vel[1]
        dt = 1/20


        for num in range(10):
            O = random.uniform(0,6.28)
            s = random.uniform(0,0.5)
            Ot = math.atan2(dR,dC) + O
            newdR = dR
            newdC = dC
            newR = R1
            newC = C1
            for n in range(1,21):
                newdR = newdR + (dt * s * math.cos(Ot))
                newdC = newdC + (dt * s * math.sin(Ot))
                newR = newR + dt* newdR
                newC = newC + dt*newdC
                if 0 > newC or newC > self.col:
                    break
                if 0 > newR or newR > self.row:
                    break
                if self.maze[int(newR)][int(newC)] =="#":
                    break
            distance = math.sqrt((newR - R2)**2+(newC - C2)**2)
            if distance < closest:
                newS = s
                newO = O
        return [newO,newS,newdR,newdC]


    def getNearest(self,new):
        """
        Returns nearest node that can actually reach or None
        """
        Nearest_node = None
        minDist = float("inf")

        for n in self.visited:
            control = self.isThruObstacle(n,new)
            if control[0] is None:
                continue

            dist = math.sqrt((new[0]-n.pos[0])**2+(new[1]-n.pos[1])**2)
            if dist < minDist:
                minDist = dist
                Nearest_node = n
        return [Nearest_node, control]

    def addPos(self,new,old,control,velo):
        """
        wrapper for adding to list
        """
        new = node(old,new[0],new[1],velo[0],velo[1],control[0],control[1])
        self.visited.append(new)

    def solve(self):
        """
        Orchestrates solving
        Get Rand -> check if obs -> get nearest and traj -> add to list -> check if goal
        """
        while True:
            self.counter += 1

            candidate_pos = self.randomPosition()
            if self.isInObstacle(candidate_pos):
                continue
            nearest = self.getNearest(candidate_pos)
            if nearest[0] is None:
                continue
            nearest_pos = nearest[0]
            control = nearest[1][0:2]
            velo = nearest[1][2:]
            
            self.addPos(candidate_pos,nearest_pos,control,velo)
            distance = math.sqrt((candidate_pos[0]-self.sR)**2+(candidate_pos[1]-self.sC)**2)
            if distance <= 0.1: 
                break
        self.path()
def main():
    col = int(input())
    row = int(input())
    maze = []
    for n in range(row):
        line = input()
        maze.append([char for char in line])
    sX = float(input())
    sY = float(input())
    gX = float(input())
    gY = float(input())
    grid = World(row,col,maze,sX,sY,gX,gY)
    grid.solve()
if __name__ == "__main__":
    main()
