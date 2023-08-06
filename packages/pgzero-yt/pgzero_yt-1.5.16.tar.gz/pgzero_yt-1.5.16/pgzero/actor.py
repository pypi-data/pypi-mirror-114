import pygame
from PIL import Image
import os
from math import radians, sin, cos, atan2, degrees, sqrt
from . import game
from . import loaders
from . import rect
from . import spellcheck
import operator
from random import randint

ANCHORS = {
    'x': {
        'left': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'right': 1.0,
    },
    'y': {
        'top': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'bottom': 1.0,
    }
}


def calculate_anchor(value, dim, total):
    if isinstance(value, str):
        try:
            # print(f'total:{total * ANCHORS[dim][value]}')
            return total * ANCHORS[dim][value]
        except KeyError:
            raise ValueError(
                '%r is not a valid %s-anchor name' % (value, dim)
            )
    return float(value)


# These are methods (of the same name) on pygame.Rect
SYMBOLIC_POSITIONS = set((
    "topleft", "bottomleft", "topright", "bottomright",
    "midtop", "midleft", "midbottom", "midright",
    "center",
))

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None


def transform_anchor(ax, ay, w, h, angle):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

    sintheta = sin(theta)
    costheta = cos(theta)

    # Dims of the transformed rect
    tw = abs(w * costheta) + abs(h * sintheta)
    th = abs(w * sintheta) + abs(h * costheta)

    # Offset of the anchor from the center
    cax = ax - w * 0.5
    cay = ay - h * 0.5

    # Rotated offset of the anchor from the center
    rax = cax * costheta - cay * sintheta
    ray = cax * sintheta + cay * costheta

    return (
        tw * 0.5 + rax,
        th * 0.5 + ray
    )


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [a for a in dir(rect.ZRect) if not a.startswith("_")]

    _anchor = _anchor_value = (0, 0)
    _angle = 0.0

    def __init__(self, image, pos=POS_TOPLEFT, Size=100, anchor=ANCHOR_CENTER, **kwargs):
        self._handle_unexpected_kwargs(kwargs)
        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later
        self.flip = True
        self._size = Size
        self._group = []
        self.image = image
        self._init_position(pos, anchor, **kwargs)

    def __getattr__(self, attr):
        # print(attr)
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """Assign rect attributes to the underlying rect."""
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return setattr(self._rect, attr, value)
        else:
            # Ensure data descriptors are set normally
            return object.__setattr__(self, attr, value)

    def __iter__(self):
        return iter(self._rect)

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return

        for found, suggested in spellcheck.compare(
                unexpected_kwargs, self.EXPECTED_INIT_KWARGS):
            raise TypeError(
                "Unexpected keyword argument '{}' (did you mean '{}'?)".format(
                    found, suggested))

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in SYMBOLIC_POSITIONS}

        if not pos and not symbolic_pos_args:
            # No positional information given, use sensible top-left default
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError("'pos' argument cannot be mixed with 'topleft', 'topright' etc. argument.")
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError("No position-setting keyword arguments ('topleft', 'topright' etc) found.")
        if len(symbolic_pos_dict) > 1:
            raise TypeError("Only one 'topleft', 'topright' etc. argument is allowed.")

        setter_name, position = symbolic_pos_dict.popitem()
        setattr(self, setter_name, position)

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._calc_anchor()

    def _calc_anchor(self):
        # 计算锚点
        # print(self._anchor_value)
        ax, ay = self._anchor_value
        # print(f"ax:{ax},ay:{ay}")
        # print(f'self.width:{self.width},self.height:{self.height}')
        ow, oh = self._orig_surf.get_size()
        # print(f"ow:{ow},oh:{oh}")
        ax = calculate_anchor(ax, 'x', ow)
        ay = calculate_anchor(ay, 'y', oh)
        self._untransformed_anchor = ax, ay
        if self._angle == 0.0:
            self._anchor = self._untransformed_anchor
        else:
            self._anchor = transform_anchor(ax, ay, ow, oh, self._angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        if self.flip:
            self._surf = pygame.transform.rotate(self._orig_surf, angle)
            p = self.pos
            self.width, self.height = self._surf.get_size()
            w, h = self._orig_surf.get_size()
            ax, ay = self._untransformed_anchor
            self._anchor = transform_anchor(ax, ay, w, h, angle)
            self.pos = p

    @property
    def pos(self):
        px, py = self.topleft
        ax, ay = self._anchor
        return px + ax, py + ay

    @pos.setter
    def pos(self, pos):
        px, py = pos
        ax, ay = self._anchor
        self.topleft = px - ax, py - ay

    @property
    def x(self):
        ax = self._anchor[0]
        return self.left + ax

    @x.setter
    def x(self, px):
        self.left = px - self._anchor[0]

    @property
    def y(self):
        ay = self._anchor[1]
        return self.top + ay

    @y.setter
    def y(self, py):
        self.top = py - self._anchor[1]

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._orig_surf = self._surf = loaders.images.load(image)
        self._w, self._h = self._surf.get_size()
        self._orig_surf = self._surf = pygame.transform.scale(self._surf, (
            int(self._w * self._size / 100), int(self._h * self._size / 100))).convert_alpha()
        self._w, self._h = self._surf.get_size()
        self._update_pos()
        # self.angle = p

    def _update_pos(self):
        p = self.pos  # 保存坐标
        self.width, self.height = self._surf.get_size()  # 获得宽\高
        self._calc_anchor()  # 计算锚点
        self.pos = p

    def draw(self):
        game.screen.blit(self._surf, self.topleft)

    def angle_to(self, target):
        """Return the angle from this actors position to target, in degrees."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty  # y axis is inverted from mathematical y in Pygame
        return degrees(atan2(dy, dx))

    def distance_to(self, target):
        """Return the distance from this actor's pos to target, in pixels."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)

    # yt_zxx升级
    def collidepoint(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args
        return (
                self._rect.x <= x < (self._rect.x + self._rect.w) and
                self._rect.y <= y < (self._rect.y + self._rect.h)
        )

    def colliderect(self, other):
        rect = other._rect
        return (
                self._rect.x < rect.x + rect.w and
                self._rect.y < rect.y + rect.h and
                self._rect.x + self._rect.w > rect.x and
                self._rect.y + self._rect.h > rect.y
        )

    def collidelist(self, others):
        for n, other in enumerate(others):
            if self.colliderect(other):
                return n
        else:
            return -1

    def collidelistall(self, others):
        return [n for n, other in enumerate(others) if self.colliderect(other)]

    def collidedict(self, dict, use_values=True):
        for k, v in dict.items():
            if self.colliderect(v if use_values else k):
                return k, v

    def collidedictall(self, dict, use_values=True):
        val = operator.itemgetter(1 if use_values else 0)
        return [i for i in dict.items() if self.colliderect(val(i))]

    def collidemask(self, others):
        # print(self._rect)
        xoffset = others._rect[0] - self._rect[0]
        yoffset = others._rect[1] - self._rect[1]
        try:
            leftmask = self.mask
        except AttributeError:
            leftmask = pygame.mask.from_surface(self._surf)
        try:
            rightmask = others.mask
        except AttributeError:
            rightmask = pygame.mask.from_surface(others._surf)
        return leftmask.overlap(rightmask, (int(xoffset), int(yoffset)))

    def move(self, steps):
        self.x -= steps * sin(radians(self.angle))
        self.y -= steps * cos(radians(self.angle))

    def face_to(self, target):
        self.angle = self.angle_to(target) - 90

    def in_the_edge(self):
        self._bounds = game.screen.bounds()
        if self.x > self._bounds[2]:
            self.x = self._bounds[2]
        if self.x < 0:
            self.x = 0
        if self.y > self._bounds[3]:
            self.y = self._bounds[3]
        if self.y < 0:
            self.y = 0

    def out_of_edge(self):
        self._bounds = game.screen.bounds()
        return not (0 - self._w < self.x < self._bounds[2] + self._w and 0 - self._h < self.y < self._bounds[
            3] + self._h)

    @property
    def Size(self):
        return self._size

    @Size.setter
    def Size(self, new_size):
        self._size = new_size
        p = self.angle
        self.angle = 0
        w, h = self._orig_surf.get_size()
        self._orig_surf = self._surf = pygame.transform.scale(self._surf,
                                                              (int(w * self._size / 100),
                                                               int(h * self._size / 100))).convert_alpha()
        self._w, self._h = self._surf.get_size()
        self._update_pos()
        self.angle = p

    def destroy(self):
        for group in self._group:
            group.remove(self)

    def yt(self):
        print("没想到吧!,我就是升级那个曾老师")


class Group(list):
    def append(self, __object: Actor) -> None:
        super().append(__object)
        __object._group.append(self)

    def draw(self):
        for i in self:
            i.draw()