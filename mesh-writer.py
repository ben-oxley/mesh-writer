#!/usr/bin/env -S uv run --script --verbose
# /// script
# requires-python = ">=3.12"
# dependencies = [
# ]
# ///

# https://forum.bambulab.com/t/how-do-you-do-the-new-obj-with-mtl-feature/75622/8

from dataclasses import dataclass
import math
from typing import Optional
import random


@dataclass
class Point3:
    x: float
    y: float
    z: float


@dataclass
class Point6:
    x: float
    y: float
    z: float
    r: float
    g: float
    b: float


@dataclass
class Point4:
    x: float
    y: float
    z: float
    w: float


@dataclass
class Face:
    vertex_indices: list[int]
    vertex_normal_indices: list[int]
    texture_vertex_indices: list[int]


@dataclass
class TexCoord:
    u: float
    v: Optional[float] = None
    w: Optional[float] = None


@dataclass
class RGB:
    r: float
    g: float
    b: float


@dataclass
class Material:
    colour: RGB


@dataclass
class Object:
    verticies: list[Point3]
    vertex_normals: list[Point3]
    faces: list[Face]
    texture_verticies: list[TexCoord]
    name: str
    material: Material


def wiggle(i, j):
    return 1.0 * math.sin(i / 20.0) + 1.0 * math.sin(j / 20.0)


def create_surface():
    """
    This function defines a 2d flat surface of 100x100 points, ((2*99*99) faces)
    """
    verticies: list[Point3] = []
    faces: list[Face] = []

    xlen = 100
    ylen = 100
    texture = []
    texture.append(TexCoord(0.0, 0.0))
    texture.append(TexCoord(1.0, 0.0))
    texture.append(TexCoord(0.0, 1.0))
    texture.append(TexCoord(1.0, 1.0))

    # Create top surface for the obj
    def create_surface(top: bool, height_offset: float):
        vertex_offset = len(verticies)
        for i in range(0, xlen):
            for j in range(0, ylen):
                verticies.append(
                    Point6(
                        i,
                        j,
                        height_offset + wiggle(i, j),
                        random.uniform(0.0, 1.0),
                        random.uniform(0.0, 1.0),
                        random.uniform(0.0, 1.0),
                    )
                )
                # Join bl, tr, br
                if i < xlen - 1 and j < ylen - 1:
                    if top:
                        faces.append(
                            Face(
                                vertex_indices=[
                                    vertex_offset + i * ylen + j,
                                    vertex_offset + i * ylen + j + 1,
                                    vertex_offset + (i + 1) * ylen + j,
                                ],
                                vertex_normal_indices=[],
                                texture_vertex_indices=[0, 1, 2],
                            )
                        )
                        faces.append(
                            Face(
                                vertex_indices=[
                                    vertex_offset + (i + 1) * ylen + j,
                                    vertex_offset + i * ylen + j + 1,
                                    vertex_offset + (i + 1) * ylen + j + 1,
                                ],
                                vertex_normal_indices=[],
                                texture_vertex_indices=[2, 1, 3],
                            )
                        )
                    else:
                        faces.append(
                            Face(
                                vertex_indices=[
                                    vertex_offset + i * ylen + j,
                                    vertex_offset + (i + 1) * ylen + j,
                                    vertex_offset + i * ylen + j + 1,
                                ],
                                vertex_normal_indices=[],
                                texture_vertex_indices=[0, 1, 2],
                            )
                        )
                        faces.append(
                            Face(
                                vertex_indices=[
                                    vertex_offset + (i + 1) * ylen + j,
                                    vertex_offset + (i + 1) * ylen + j + 1,
                                    vertex_offset + i * ylen + j + 1,
                                ],
                                vertex_normal_indices=[],
                                texture_vertex_indices=[2, 1, 3],
                            )
                        )

    create_surface(False, 10.0)
    create_surface(True, 0.0)

    def create_sides():
        # Top and bottom
        for i in range(0, ylen - 1):
            faces.append(
                Face(
                    vertex_indices=[
                        i,
                        i + 1,
                        xlen * ylen + i,
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )
            faces.append(
                Face(
                    vertex_indices=[
                        xlen * ylen + i + 1,
                        xlen * ylen + i,
                        i + 1,
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[2, 3, 0],
                )
            )
            # Top Side
            faces.append(
                Face(
                    vertex_indices=[
                        ((xlen - 1) * ylen) + i + 1,
                        ((xlen - 1) * ylen) + i,
                        (xlen * ylen) + (((xlen - 1) * ylen) + i),
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )
            faces.append(
                Face(
                    vertex_indices=[
                        ((xlen - 1) * ylen) + i + 1,
                        (xlen * ylen) + (((xlen - 1) * ylen) + i),
                        (xlen * ylen) + (((xlen - 1) * ylen) + i + 1),
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )
        for i in range(0, xlen - 1):
            # Left Side
            faces.append(
                Face(
                    vertex_indices=[
                        (i + 1) * ylen,
                        i * ylen,
                        xlen * ylen + i * ylen,
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )
            faces.append(
                Face(
                    vertex_indices=[
                        xlen * ylen + i * ylen,
                        xlen * ylen + (i + 1) * ylen,
                        (i + 1) * ylen,
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[2, 3, 0],
                )
            )
            # Right Side
            faces.append(
                Face(
                    vertex_indices=[
                        (ylen - 1) + i * ylen,
                        (ylen - 1) + (i + 1) * ylen,
                        xlen * ylen + i * ylen + (ylen - 1),
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )
            faces.append(
                Face(
                    vertex_indices=[
                        (ylen - 1) + (i + 1) * ylen,
                        xlen * ylen + (ylen - 1) + (i + 1) * ylen,
                        xlen * ylen + i * ylen + (ylen - 1),
                    ],
                    vertex_normal_indices=[],
                    texture_vertex_indices=[0, 1, 2],
                )
            )

        # Bottom side will stitch together node 0,1,x*y,x*y+1 etc e.g in a (4x,3y) 0,1,12,13
        # Top side will stitch together (x*(y-1)),(x*(y-1)+1), x*y+(x*(y-1)) and x*y+(x*(y-1)+1) e.g. in a (4x,3y) 8,9,20,21
        # Left side will stitch together 0,x,x*y,x*y+x
        # Right side will stitch together x-1,x*y-1,x*y+x-1,x*y+x

        side_offset = xlen * ylen

    create_sides()

    material = Material(colour=RGB(r=255.0, g=255.0, b=255.0))
    return Object(
        name="surface",
        material=material,
        verticies=verticies,
        faces=faces,
        vertex_normals=[],
        texture_verticies=texture,
    )


def write_object(obj: Object, filename: str):
    obj_name = obj.name.removesuffix(".obj")
    with open(filename, "w") as f:
        f.write("# Generated by uv script\n")
        f.write(f"o {obj_name}\n")
        f.write(f"mtllib {obj_name}.mtl\n")
        for v in obj.verticies:
            if isinstance(v, Point3):
                f.write(f"v {v.x} {v.y} {v.z}\n")
            elif isinstance(v, Point4):
                f.write(f"v {v.x} {v.y} {v.z} {v.w}\n")
            elif isinstance(v, Point6):
                f.write(f"v {v.x} {v.y} {v.z} {v.r} {v.g} {v.b}\n")
        for n in obj.vertex_normals:
            f.write(f"vn {n.x} {n.y} {n.z}\n")
        for t in obj.texture_verticies:
            if t.v is not None and t.w is not None:
                f.write(f"vt {t.u} {t.v} {t.w}\n")
            else:
                f.write(f"vt {t.u} {t.v or 0}\n")

        f.write(f"g {obj_name}\n")
        f.write(f"usemtl {obj_name}\n")
        print(len(obj.faces), "faces")
        for face in obj.faces:
            face.texture_vertex_indices = []
            if (
                len(face.vertex_normal_indices) == 0
                and len(face.texture_vertex_indices) == 0
            ):
                # If no normals or texture coordinates, just use vertex indices
                indices = " ".join([f"{o+1}" for o in face.vertex_indices])
                f.write(f"f {indices}\n")
                continue
            if len(face.texture_vertex_indices) == 0:
                indices = " ".join(
                    [
                        f"{o[0]+1}//{o[1]+1}"
                        for o in zip(face.vertex_indices, face.vertex_normal_indices)
                    ]
                )
                f.write(f"f {indices}\n")
                continue
            if len(face.vertex_normal_indices) == 0:
                indices = " ".join(
                    [
                        f"{o[0]+1}/{o[1]+1}"
                        for o in zip(face.vertex_indices, face.texture_vertex_indices)
                    ]
                )
                f.write(f"f {indices}\n")
                continue
            # Remaining valid condition is all are present
            indices = " ".join(
                [
                    f"{o[0]+1}/{o[1]+1}/{o[2]+1}"
                    for o in zip(
                        face.vertex_indices,
                        face.texture_vertex_indices,
                        face.vertex_normal_indices,
                    )
                ]
            )
            f.write(f"f {indices}\n")
            continue
    with open(filename.replace(".obj", ".mtl"), "w") as f:
        f.write(f"newmtl {obj_name}\n")
        colour = obj.material.colour
        f.write(f"  Kd {colour.r} {colour.g} {colour.b}")


write_object(create_surface(), "surface.obj")
