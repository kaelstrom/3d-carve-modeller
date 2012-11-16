from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL import GL as gl
import sys, numpy, time, random, math
from math import fmod, sin, cos
from camera_functions import lookInSphere

winWidth=1280
winHeight=720

#These three defines exist in OpenGL.GL, but does not correspond to those used here
GL_GEOMETRY_SHADER_EXT       = 0x8DD9
GL_GEOMETRY_INPUT_TYPE_EXT   = 0x8DDB
GL_GEOMETRY_OUTPUT_TYPE_EXT  = 0x8DDC
GL_GEOMETRY_VERTICES_OUT_EXT = 0x8DDA

#Define the missing glProgramParameteri method
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

    gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, upX, upY, upZ);

    #glRotate( theta*15.0, 0.0,0.0,1.0 )
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

mouseDrag=mouseDragX=mouseDragY=eyeX=eyeY=eyeZ=upX=upY=upZ=cam_phi=0
cam_theta=90
cam_r=100
def onMousePress(button, state, x, y):
    global mouseDrag,mouseDragX,mouseDragY
    if button == GLUT_LEFT_BUTTON:
        mouseDrag = (state == GLUT_DOWN)
    if mouseDrag:
        mouseDragX = x
        mouseDragY = y
        return
    
def onMouseMove(x, y):
    global mouseDrag,mouseDragX,mouseDragY
    global eyeX,eyeY,eyeZ,upX,upY,upZ,cam_theta,cam_phi,cam_r
    if not mouseDrag: return
    #Mouse point to angle conversion
    #cam_theta = (360.0/winHeight)*y*3.0#3.0 rotations possible
    #cam_phi = (360.0/winWidth)*x*3.0
    cam_phi += 360.0*(mouseDragX - x)/winWidth*2.0
    cam_theta += 360.0*(mouseDragY - y)/winHeight*2.0
    mouseDragX = x
    mouseDragY = y
    #Restrict the angles within 0~360 deg (optional)
    if cam_theta > 360:
        cam_theta = fmod(cam_theta,360.0)
    if cam_phi > 360:
        cam_phi = fmod(cam_phi,360.0)
    newValues = lookInSphere(cam_r,cam_phi,cam_theta)
    eyeX = newValues[0]
    eyeY = newValues[1]
    eyeZ = newValues[2]
    upX = newValues[3]
    upY = newValues[4]
    upZ = newValues[5]
    glutPostRedisplay()
    
def onKeyPress(key, x, y):
    global eyeX,eyeY,eyeZ,upX,upY,upZ,cam_theta,cam_phi,cam_r
    if key == chr(27):
        sys.exit()
    if key == 'z':
        cam_r = max(0,cam_r-10)
    if key == 'Z':
        cam_r += 10
    newValues = lookInSphere(cam_r,cam_phi,cam_theta)
    eyeX = newValues[0]
    eyeY = newValues[1]
    eyeZ = newValues[2]
    upX = newValues[3]
    upY = newValues[4]
    upZ = newValues[5]
    
def onKeySpecialPress(key, x, y):
    global eyeX,eyeY,eyeZ,upX,upY,upZ,cam_theta,cam_phi,cam_r
    if key == GLUT_KEY_LEFT:
        cam_phi = (math.floor(cam_phi/45.0)+1.0)*45.0
    if key == GLUT_KEY_RIGHT:
        cam_phi = (math.ceil(cam_phi/45.0)-1.0)*45.0
    if key == GLUT_KEY_UP:
        cam_theta = (math.floor(cam_theta/45.0)+1.0)*45.0
    if key == GLUT_KEY_DOWN:
        cam_theta = (math.ceil(cam_theta/45.0)-1.0)*45.0
    #Restrict the angles within 0~360 deg (optional)
    if cam_theta > 360:
        cam_theta = fmod(cam_theta,360.0)
    if cam_phi > 360:
        cam_phi = fmod(cam_phi,360.0)
    newValues = lookInSphere(cam_r,cam_phi,cam_theta)
    eyeX = newValues[0]
    eyeY = newValues[1]
    eyeZ = newValues[2]
    upX = newValues[3]
    upY = newValues[4]
    upZ = newValues[5]
    
def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE )
    glutInitWindowSize(winWidth, winHeight)
    #Open a window
    glutCreateWindow("Glut test window")
    
    glutReshapeFunc( reshape )
    glutDisplayFunc( display )
    glutMouseFunc( onMousePress )
    glutMotionFunc( onMouseMove )
    glutKeyboardFunc( onKeyPress )
    glutSpecialFunc( onKeySpecialPress )
    glutIdleFunc( my_idle )
    glEnable( GL_DEPTH_TEST )
    glClearColor( 1,1,1,0 )
    
    define_shader()
    
    global POINTS
    global COLORS
    global STATE
    COLORS = numpy.ones( cube_length**3*3 ).reshape( (-1,3) )
    POINTS = numpy.ones( cube_length**3*3 ).reshape( (-1,3) )
    STATE  = 2*numpy.ones( cube_length**3*3 ).reshape( (-1,3) )  

    for i in range(cube_length):
        for j in range(cube_length):
            for k in range(cube_length):
                #POINTS[i*cube_length**2+j*cube_length+k] = [i+i*j,j+j*k,k+k*i]
                POINTS[i*cube_length**2+j*cube_length+k] = [i+0.5-cube_length/2,j+0.5-cube_length/2,k+0.5-cube_length/2]
                COLORS[i*cube_length**2+j*cube_length+k] = [i*1.0/cube_length,j*1.0/cube_length,k*1.0/cube_length]
                if i == 0 or j == 0 or k == 0 or i == cube_length-1 or j == cube_length-1 or k == cube_length-1:
                    STATE[i*cube_length**2+j*cube_length+k] = 1#set as external point, internal are 2, removed are 0
                    
    global eyeX,eyeY,eyeZ,upX,upY,upZ,cam_theta,cam_phi,cam_r
    newValues = lookInSphere(cam_r,cam_phi,cam_theta)
    eyeX = newValues[0]
    eyeY = newValues[1]
    eyeZ = newValues[2]
    upX = newValues[3]
    upY = newValues[4]
    upZ = newValues[5]
    glutMainLoop();
    
init()