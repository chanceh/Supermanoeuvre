import rhinoscriptsyntax as rs
import random



class Rover(object):
    """
    A simple object class that walks on the screen!
    """

    def __init__(self, GUID_TERRAIN, CRV, SPEED=1):
        # CLASS PROPERTIES
        pt_from          = rs.CurveStartPoint(CRV)
        pt_to            = rs.CurveEndPoint(CRV)
        
        self.pos         = pt_from 
        self.vel         = rs.VectorSubtract(pt_to, pt_from)
        self.vel         = rs.VectorUnitize(self.vel)
        self.vel         = rs.VectorScale(self.vel, SPEED)
        self.terrain     = GUID_TERRAIN
        self.proj_points = []
        
        self.depth_scans = []    # a list store scan data
        
        self.history     = []    # remember everywhere i have been
        self.history.append( self.pos )
        self.render()            #drawing the 0-text dot
        self.z_distances = []
        self.x_pos = []
        
        self.z_difference = []
        self.x_difference = []



    # CLASS BEHAVIORS
    def update(self):
        """
        This is the primary run method
        i.e. call any other methods from here
        """
        
        self.measure_terrain()
        self.respond()
        self.move()
        self.render()
        #self.renderhistory()


    def measure_terrain(self):
        #i = random.randrange(1,100,1)
        #print i
        #PROJECT POINT TO SURFACE
        proj_points = rs.ProjectPointToSurface(self.pos,self.terrain,(0,0,-1))
        
        #STOP THE FUNCTION IF THE POINT IS OFF THE SRF
        try: proj_point = proj_points[0]
        except: return
        self.proj_points.append(proj_point)
        #rs.AddPoint(proj_points[0])   #show points
        #print proj_points
        #print self.proj_points
        
        #FIND Z DISTANCE
        z_distance = (self.pos[2]-proj_point[2]) 
        self.z_distances.append(z_distance)
        self.z_difference = 0
        self.x_difference = 0
       
        #FIND Z DIFFERENCE
        for n in range (len(self.z_distances)):
            if n > 0:
                self.z_difference = self.z_distances[n] - self.z_distances[n-1]
                #self.z_difference = self.z_difference*(i/10)
        #FIND X DIFFERENCE
        self.x_pos.append(self.pos[0])
        for m in range (len(self.x_pos)):
            if m > 0:
                self.x_difference = self.x_pos[m] - self.x_pos[m-1]
        #print self.z_distances[n],"-", self.z_distances[n-1], "=", self.z_difference


    def respond(self):
        i = random.uniform(1,100)
        
        #ROTATE VECTORS HEADING LEFT TO THE RIGHT - IE TURN RIGHT
        if self.x_difference < 0:
            if self.z_difference < 0:
                self.vel = rs.VectorRotate(self.vel, -i, (0,0,1))
        
        #ROTATE VECTORS HEADING RIGHT TO THE LEFT - IE TURN LEFT
        elif self.x_difference > 0:
            if self.z_difference < 0:
                self.vel = rs.VectorRotate(self.vel, i, (0,0,1))
        
        # ROTATE VECTORS GOING STRAIGHT
        else:
            if self.z_difference < 0:
                self.vel = rs.VectorRotate(self.vel, -45, (0,0,1))
        #print x_difference


    def move(self):
        
        xx = self.pos[0] + self.vel[0]
        yy = self.pos[1] + self.vel[1]
        zz = self.pos[2] + self.vel[2]
        self.pos = [xx,yy,zz]
        self.history.append( self.pos )


    def setpos(self, xx, yy, zz):
        self.pos = [xx,yy,zz]
    def render(self):
        """
        draws a text dot object at our current location
        """
        
        #rs.AddTextDot( len(self.history)-1, self.pos)
        #draw a curve through all points


    def renderhistory(self):
        """
        draws a curve through all the positions
        in my history list
        """
        
        proj_points_new = []
        circle1 = []
        
        #ADD CURVE
        for i in range (len(self.proj_points)):
            if i%10 == 0:
                if self.proj_points[i] is not None:
                    proj_points_new.append(self.proj_points[i])
        try: self.crv1 = rs.AddCurve(proj_points_new,3)
        except: pass
        #ADD SWEEP GEOMETRY
        #print (len(self.z_distances))
        #self.crv1_start = rs.CurveStartPoint(self.crv1)
        #divide_crv = rs.DivideCurve(self.crv1, (len(self.z_distances))
        #print divide_crv
        #proj_pipe = rs.AddPipe(self.crv1,(len(self.z_distances)),self.z_distances, cap=2)
        #crv1_lenght = rs.CurveLength(self.crv1)
        #print crv1_lenght
        try:proj_pipe = rs.AddPipe(self.crv1,0,.25, cap=2)
        except:pass



    def rendersurface(self):
        """
        get the curves 1, 2
        copy the curves up n distance in the z
        select curves 1 and 2 only
        loft yjrm
        """
        i = random.uniform(1,100)
        
        print self.crv1
        self.crv1 
        movecrv1 = rs.MoveObject(self.crv1)
        #    if movecrv1
        #        tr



def main():
    # the user needs to input
    brep_terrain = rs.GetObject("Gimme BREP", rs.filter.polysurface )
    start_crvs    = rs.GetObjects("Gimme ROVER CURVE", rs.filter.curve )
    numsteps     = 250
    speed        = 1 
    
    # rover stuff
    for crv in start_crvs:
        r = Rover(brep_terrain, crv, speed)
    
        # update the rover
        for i in range(numsteps):
            r.update()
        r.renderhistory()
        #r.rendersurface()
   

if(__name__ == "__main__"):
    main()