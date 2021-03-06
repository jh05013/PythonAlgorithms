from math import sin, cos, tan, pi, asin, acos, atan
from functools import cmp_to_key, total_ordering
def sgn(x): return (0<x) - (x<0)

## Point ################################################

@total_ordering
class Pnt:
    def __init__(_, x, y): _.x = x; _.y = y
    def __repr__(_): return f"({_.x}, {_.y})"
    
    # Basic ops
    def sq(_): return _.x**2 + _.y**2
    def __abs__(_): return (_.x**2 + _.y**2)**.5
    def __le__(_, o): return (_.x, _.y) <= (o.x, o.y)
    
    # Scalar ops
    def __mul__(_, d): return Pnt(d*_.x, d*_.y)
    def __rmul__(_, d): return Pnt(_.x*d, _.y*d)
    def __truediv__(_, d): return Pnt(_.x/d, _.y/d)
    def __floordiv__(_, d): return Pnt(_.x//d, _.y//d)
    
    # Vector ops
    def __eq__(_, q): return _.x==q.x and _.y==q.y
    def __add__(_, q): return Pnt(_.x+q.x, _.y+q.y)
    def __sub__(_, q): return Pnt(_.x-q.x, _.y-q.y)

# Vector functions
def dot(p, q): return p.x*q.x + p.y*q.y
def cross(p, q): return p.x*q.y - p.y*q.x
def angle(p, q): return acos(max(-1, min(1, dot(p,q)/abs(p)/abs(q))))

# Transformations
def scale(c, p, factor): return c + (p-c)*factor
def rot(p, t): # theta
    return Pnt(p.x*cos(t)-p.y*sin(t), p.x*sin(t)+p.y*cos(t))
def rotc(c, p, theta):
    return c + rot(p-c, theta)
def rot90(p): return Pnt(-p.y, p.x)
def linear_trans(p, q, r, np, nq):
    pq = q-p; N = Pnt(cross(pq, nq-np), dot(pq, nq-np))
    return np + Pnt(cross(r-p, N), dot(r-p, N)) / pq.sq()

# CCW
def orient(a, b, c): return cross(b-a, c-a) # >0 ccw
def ccw(a, b, c): return sgn(cross(b-a, c-a)) # 1 ccw
def anglechange(p, q):
    theta = angle(p, q)
    return theta if orient(p,Pnt(0,0),q)<=0 else 2*pi-theta
def anglediff(p, q):
    theta = angle(p, q)
    return min(theta, 2*pi-theta)
def anglechangec(c, p, q):
    return anglechange(p-c, q-c)
def anglediffc(c, p, q):
    return anglediff(p-c, q-c)

# Sort by angle
def half(p): return p.y>0 or (p.y==0 and p.x<0)
@cmp_to_key
def halfcmp(p, q):
    A = (half(p), 0, p.sq()); B = (half(q), cross(p,q), q.sq())
    return 0 if A==B else (-1 if A<B else 1)
def polarsort(O, pnts):
    return [x+O for x in sorted([x-O for x in pnts], key=halfcmp)]

## Straight lines #######################################

class Line:
    # v[0]y = v[1]x+c
    def __init__(_, v, c):
        if type(c) == Pnt: _.v = c-v; _.c = cross(_.v,v)
        else: _.v = v; _.c = c
    def __repr__(_): return f"{_.v}+{_.c}"
    
    # Point ops
    def side(_, p): return cross(_.v,p) - _.c # >0 ccw
    def dist(_, p): return abs(_.side(p)) / abs(_.v)
    def sqdist(_, p): return abs(_.side(p))**2 // _.v.sq()
    def perpline(_, p): return Line(p, p+rot90(_.v))
    def proj(_, p): return p - rot90(_.v)*_.side(p)/_.v.sq()
    def refl(_, p): return p - 2*rot90(_.v)*_.side(p)/_.v.sq()
    
    # Vector ops
    def translate(_, v): return Line(_.v, _.c+cross(_.v,v))
    def shiftleft(_, d): return Line(_.v, _.c+dist*abs(_.v))

def Line_abc(a, b, c): return Line(Pnt(b,-a), c)

# Intersection
def line_inter(L1, L2):
    d = cross(L1.v, L2.v)
    if d == 0: return False
    return (L2.v*L1.c - L1.v*L2.c) / d

# Sort by projection
def projsort(L, pnts):
    return sorted(pnts, key = lambda p: dot(L.v, p))

## Line segments ########################################

def on_seg(a, b, p):
    return orient(a,b,p) == 0 and dot(a-p, b-p) <= 0

# segment intersections
def seg_inter_proper(a, b, c, d):
    oa, ob = orient(c,d,a), orient(c,d,b)
    oc, od = orient(a,b,c), orient(a,b,d)
    if oa*ob >= 0 or oc*od >= 0: return False
    return (a*ob - b*oa) / (ob-oa)

def seg_inters(a, b, c, d):
    res = []
    P = seg_inter_proper(a, b, c, d)
    if P: res.append(P)
    if on_seg(c,d,a): res.append(a)
    if on_seg(c,d,b): res.append(b)
    if on_seg(a,b,c): res.append(c)
    if on_seg(a,b,d): res.append(d)
    return res

# distances
def seg_pnt_dist(a, b, p):
    if a == b: return abs(p-a)
    q = Line(a,b).proj(p)
    if dot(q-a, q-b) <= 0: return Line(a,b).dist(p)
    return min(abs(p-a), abs(p-b))

def seg_seg_dist(a, b, c, d):
    if seg_inter_proper(a, b, c, d): return 0
    return min(seg_pnt_dist(a,b,c), seg_pnt_dist(a,b,d),
               seg_pnt_dist(c,d,a), seg_pnt_dist(c,d,b))

## Polygon ##############################################

def isconvex(P):
    v = [ccw(P[i-2], P[i-1], P[i]) for i in range(len(P))]
    return not (1 in v and -1 in v)

def area2(P):
    # twice the area
    A = 0
    for i in range(len(P)): A+= cross(P[i-1], P[i])
    return abs(A)

def inpoly_convex(p, P, strict):
    Q = [ccw(P[i], P[i-1], p) for i in range(len(P))]
    if strict and (0 in Q): return False
    return 1 not in Q or -1 not in Q

def inpoly(P, strict):
    raise NotImplementedError

## Circle ###############################################

class Circle:
    def __init__(_, p, r): _.p=p; _.r=r
    def __repr__(_): return f"{_.p}O<{_.r}>"
    def angle(_, q): return angle(Pnt(1,0), q-_.p)

def circumcircle(a, b, c):
    b = b-a; c = c-a
    assert cross(b, c) != 0
    p = a + rot90(b*c.sq() - c*b.sq())/cross(b,c)/2
    return Circle(p, abs(a-p))

# tangent
def point_circle_tangent(p, C):
    d = abs(C.p-p)
    theta = asin(C.r / d)
    ans = []
    for u in [-theta, theta]:
        V = rotc(p, O, u)
        ans.append(scale(p, V, (d**2-C.r**2)**.5 / d))
    return ans

## Convex hull ##########################################

def convexhull(P, split=False):
    U = []; L = []; P.sort()
    for q in P:
        while len(U)>1 and ccw(U[-2], U[-1], q) >= 0: U.pop()
        while len(L)>1 and ccw(L[-2], L[-1], q) <= 0: L.pop()
        U.append(q); L.append(q)
    if split: return U, L
    return U+L[-2:0:-1]

######## MAIN CODE BELOW ################
