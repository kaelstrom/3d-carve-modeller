from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL import GL as gl
import random
import time
import numpy
import math
from math import fmod, sin, cos

#These three defines exist in OpenGL.GL, but does not correspond to those used here
GL_GEOMETRY_SHADER_EXT       = 0x8DD9
GL_GEOMETRY_INPUT_TYPE_EXT   = 0x8DDB
GL_GEOMETRY_OUTPUT_TYPE_EXT  = 0x8DDC
GL_GEOMETRY_VERTICES_OUT_EXT = 0x8DDA
cam_r=150
cam_theta=270
cam_phi=180

# Define the missing glProgramParameteri method
_glProgramParameteri = None
def glProgramParameteri( program, pname, value  ):
    global _glProgramParameteri
    if not _glProgramParameteri:
        import ctypes
        # Open the opengl32.dll
        gldll = ctypes.windll.opengl32
        # define a function pointer prototype of *(GLuint program, GLenum pname, GLint value)
        prototype = ctypes.WINFUNCTYPE( ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int )
        # Get the win gl func adress
        fptr = gldll.wglGetProcAddress( 'glProgramParameteriEXT' )
        if fptr==0:
            raise Exception( "wglGetProcAddress('glProgramParameteriEXT') \
                         returned a zero adress, which will result in a nullpointer error if used.")
        _glProgramParameteri = prototype( fptr )
    _glProgramParameteri( program, pname, value )

# Define the missing glCreateShaderObject method
_glCreateShaderObject = None
def glCreateShaderObject( shadertype ):
    global _glCreateShaderObject
    if not _glCreateShaderObject:
        import ctypes
        # Open the opengl32.dll
        gldll = ctypes.windll.opengl32
        # define a function pointer prototype of *(GLuint program, GLenum pname, GLint value)
        prototype = ctypes.WINFUNCTYPE( ctypes.c_int, ctypes.c_uint )
        # Get the win gl func adress
        fptr = gldll.wglGetProcAddress( 'glCreateShaderObjectARB' )
        if fptr==0:
            raise Exception( "wglGetProcAddress('glCreateShaderObjectARB') \
                          returned a zero adress, which will result in a nullpointer error if used.")
        _glCreateShaderObject = prototype( fptr )
    return _glCreateShaderObject( shadertype )

vert = '''
void main(){
    gl_FrontColor = gl_Color;
    gl_Position = ftransform();
}
'''

geom = '''#version 120 
#extension GL_EXT_geometry_shader4 : enable 
const float radius = 0.5;
varying out vec2 coord;

void main() 
{
  gl_FrontColor = gl_FrontColorIn[0];

  coord = vec2( -1,-1 );
  gl_Position = (gl_PositionIn[0] + gl_ProjectionMatrix * vec4(-radius,-radius,0,0) );
  EmitVertex();
  coord = vec2( -1,1 );
  gl_Position = (gl_PositionIn[0] + gl_ProjectionMatrix * vec4(-radius,radius, 0,0) );
  EmitVertex();
  coord = vec2( 1,-1 );
  gl_Position = (gl_PositionIn[0] + gl_ProjectionMatrix * vec4( radius,-radius, 0,0) );
  EmitVertex();
  coord = vec2( 1,1 );
  gl_Position = (gl_PositionIn[0] + gl_ProjectionMatrix * vec4( radius,radius, 0,0) );
  EmitVertex();  
  EndPrimitive();
}
'''
frag = '''
in vec2 coord;
void main(){
    vec4 color = gl_Color;
    color.a = 1.0-length( coord );
    if (color.a<0.0) discard;

    // A VERY FAKE "lighting" model
    float d = dot( normalize(vec3(coord,1.0)), vec3( 0.19, 0.19, 0.96225 ) );
    color.rgb *= d*d;
    // end "lighting"
    
    gl_FragColor = color;
}
'''

theta = 0.0
delta = 0.0
cube_length = 50

def my_idle( ):
    global theta
    global delta 
    t = time.clock()
    passed = t-delta
    #theta += passed
    delta = t
    global POINTS
    #POINTS+=.1*(.5-numpy.random.random( cube_length**3*3 ).reshape( (-1,3) ))
    glutPostRedisplay()

shader_program = None
def define_shader():
    global shader_program
    shader_program = gl.glCreateProgram()   
    glProgramParameteri(shader_program, GL_GEOMETRY_INPUT_TYPE_EXT, gl.GL_POINTS )
    glProgramParameteri(shader_program, GL_GEOMETRY_OUTPUT_TYPE_EXT, gl.GL_TRIANGLE_STRIP )
    glProgramParameteri(shader_program, GL_GEOMETRY_VERTICES_OUT_EXT, 4 )

    vobj = glCreateShaderObject( GL_VERTEX_SHADER )
    glShaderSource( vobj, vert )
    glCompileShader( vobj )
    print glGetShaderInfoLog(vobj)
    glAttachShader( shader_program, vobj )
    
    gobj = glCreateShaderObject( GL_GEOMETRY_SHADER_EXT )
    glShaderSource( gobj, geom)    
    glCompileShader( gobj )
    print glGetShaderInfoLog(gobj)
    glAttachShader( shader_program, gobj )

    fobj = glCreateShaderObject( GL_FRAGMENT_SHADER )
    glShaderSource( fobj, frag)    
    glCompileShader( fobj )
    print glGetShaderInfoLog(fobj)
    glAttachShader( shader_program, fobj )
    
    glLinkProgram( shader_program )
    print glGetProgramInfoLog(shader_program)


def reshape( width, height ):
   glViewport(0, 0, width, height);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluPerspective(65.0, width / float(height), 1, 1000 );
   glMatrixMode(GL_MODELVIEW);

POINTS = None
COLORS = None
STATE  = None
def display( ):   
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )  
   glLoadIdentity()   
   #gluLookAt( 100.0,100.0,100.0,
   #           0.0,0.0,0.0,
   #           0.0,0.0,1.0 )
   
   gluLookAt(eyeX,eyeY,eyeZ,25,25,25,upX, upY, upZ);

   glRotate( theta*15.0, 0.0,0.0,1.0 )
   #glTranslatef( 25.0,25.0,0 )
   
   #glEnable( GL_BLEND )
   glBlendFunc( GL_SRC_ALPHA, GL_ONE )
   glUseProgram( shader_program )
   glEnableClientState( GL_COLOR_ARRAY )
   glEnableClientState( GL_VERTEX_ARRAY )
   glColorPointer( 3,GL_FLOAT,0,COLORS )
   glVertexPointer(3,GL_FLOAT,0,POINTS )
   glDrawArrays( 0,0, len( POINTS ) )
  
   glutSwapBuffers()


eyeX=eyeY=eyeZ=upX=upY=upZ=0
def onMouseMove(x, y):
    global eyeX,eyeY,eyeZ,upX,upY,upZ,cam_theta,cam_phi,cam_r
    # Mouse point to angle conversion
    cam_theta = (360.0/winHeight)*y*3.0    #3.0 rotations possible
    cam_phi = (360.0/winWidth)*x*3.0

    # Restrict the angles within 0~360 deg (optional)
    if cam_theta > 360:
        cam_theta = fmod(cam_theta,360.0)
    if cam_phi > 360:
        cam_phi = fmod(cam_phi,360.0)

    # Spherical to Cartesian conversion.   
    # Degrees to radians conversion factor 0.0174532
    eyeX = cam_r * sin(cam_theta*0.0174532) * sin(cam_phi*0.0174532)
    eyeY = cam_r * cos(cam_theta*0.0174532)
    eyeZ = cam_r * sin(cam_theta*0.0174532) * cos(cam_phi*0.0174532)

    # Reduce theta slightly to obtain another point on the same longitude line on the sphere.
    dt=1.0
    eyeXtemp = cam_r * sin(cam_theta*0.0174532-dt) * sin(cam_phi*0.0174532)
    eyeYtemp = cam_r * cos(cam_theta*0.0174532-dt)
    eyeZtemp = cam_r * sin(cam_theta*0.0174532-dt) * cos(cam_phi*0.0174532)

    # Connect these two points to obtain the camera's up vector.
    upX=eyeXtemp-eyeX
    upY=eyeYtemp-eyeY
    upZ=eyeZtemp-eyeZ

    glutPostRedisplay()

winHeight=720
winWidth=1280

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE )
    glutInitWindowSize(winWidth, winHeight)
    # Open a window
    glutCreateWindow("Glut test window")
    
    glutReshapeFunc( reshape )
    glutDisplayFunc( display )
    glutMotionFunc( onMouseMove )
    glutIdleFunc( my_idle )
    glEnable( GL_DEPTH_TEST )
    glClearColor( 1,1,1,0 )

    define_shader()


    global POINTS
    global COLORS
    global STATE
    COLORS = numpy.ones( cube_length**3*3 ).reshape( (-1,3) )
    POINTS = numpy.ones( cube_length**3*3 ).reshape( (-1,3) )
    STATE  = numpy.ones( cube_length**3*3 ).reshape( (-1,3) )  

    for i in range(cube_length):
        for j in range(cube_length):
            for k in range(cube_length):
                #POINTS[i*cube_length**2+j*cube_length+k] = [i+i*j,j+j*k,k+k*i]
                POINTS[i*cube_length**2+j*cube_length+k] = [i,j,k]
                COLORS[i*cube_length**2+j*cube_length+k] = [i*1.0/cube_length,j*1.0/cube_length,k*1.0/cube_length]
     
    glutMainLoop();

init()