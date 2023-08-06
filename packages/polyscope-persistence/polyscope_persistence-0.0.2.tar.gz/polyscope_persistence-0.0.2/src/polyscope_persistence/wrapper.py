import os
import sys

import numpy as np
import polyscope as ps


class PolyscopeMesh:
    def __init__(self, name, verts, faces, smooth_shade=True, enabled=True):
        self.name = name
        self.verts = verts
        self.faces = faces
        self.smooth_shade = smooth_shade
        self.enabled = enabled
        self.scalar_quantities = []
        self.vector_quantities = []

    def register(self, ps):
        o = ps.register_surface_mesh(self.name, self.verts, self.faces, smooth_shade=self.smooth_shade, enabled=self.enabled)
        for q in self.scalar_quantities + self.vector_quantities:
            q.register(o)

    def add_vector_quantity(self, name, values, enabled=None, vectortype="standard", length=None, radius=None, color=None):
        self.vector_quantities.append(
            PolyscopeVectorQuantity(name, values, enabled=enabled, vectortype=vectortype, length=length, radius=radius, color=color))

    def add_scalar_quantity(self, name, values, enabled=None, datatype="standard", vminmax=None, cmap=None):
        self.scalar_quantities.append(PolyscopeScalarQuantity(name, values, enabled=enabled, datatype=datatype, vminmax=vminmax, cmap=cmap))


class PolyscopePointcloud:
    def __init__(self, name, points, enabled=None, radius=None, color=None, material=None):
        assert points.shape[1] == 3
        self.name = name
        self.points = points
        self.enabled = enabled
        self.radius = radius
        self.color = color
        self.material = material
        self.scalar_quantities = []
        self.vector_quantities = []

    def register(self, ps):
        o = ps.register_point_cloud(name=self.name, points=self.points, enabled=self.enabled, radius=self.radius, color=self.color,
                                    material=self.material)
        for q in self.scalar_quantities + self.vector_quantities:
            q.register(o)

    def add_vector_quantity(self, name, values, enabled=None, vectortype="standard", length=None, radius=None, color=None):
        self.vector_quantities.append(
            PolyscopeVectorQuantity(name, values, enabled=enabled, vectortype=vectortype, length=length, radius=radius, color=color))

    def add_scalar_quantity(self, name, values, enabled=None, datatype="standard", vminmax=None, cmap=None):
        self.scalar_quantities.append(PolyscopeScalarQuantity(name, values, enabled=enabled, datatype=datatype, vminmax=vminmax, cmap=cmap))


class PolyscopeVectorQuantity:
    def __init__(self, name, values, enabled=None, vectortype="standard", length=None, radius=None, color=None):
        assert values.shape[1] == 3
        self.name = name
        self.vectors = values
        self.enabled = enabled
        self.vectortype = vectortype
        self.length = length
        self.radius = radius
        self.color = color

    def register(self, obj):
        obj.add_vector_quantity(self.name, self.vectors, enabled=self.enabled, vectortype=self.vectortype, length=self.length,
                                radius=self.radius, color=self.color)


class PolyscopeScalarQuantity:
    def __init__(self, name, values, enabled=None, datatype="standard", vminmax=None, cmap=None):
        self.name = name
        self.values = values
        self.enabled = enabled
        self.datatype = datatype
        self.vminmax = vminmax
        self.cmap = cmap

    def register(self, obj):
        obj.add_scalar_quantity(self.name, self.values, enabled=self.enabled, datatype=self.datatype, vminmax=self.vminmax, cmap=self.cmap)


class PolyscopeObject:
    def __init__(self, load_state_from=None):
        self.state = {}
        if load_state_from is not None:
            self.load(load_state_from)

    def register_surface_mesh(self, name, verts, faces, smooth_shade=True, enabled=True):
        mesh = PolyscopeMesh(name, verts, faces, smooth_shade, enabled=enabled)
        self.state[name] = mesh
        return mesh

    def register_point_cloud(self, name, points, enabled=None, radius=None, color=None, material=None):
        pc = PolyscopePointcloud(name, points, enabled=enabled, radius=radius, color=color, material=material)
        self.state[name] = pc
        return pc

    def screenshot(self, filename, transparentBG=True):
        ps.init()
        ps.remove_all_structures()
        for k, v in self.state.items():
            v.register(ps)
        ps.screenshot(filename, transparentBG)

    def show(self, title=None):

        if title is not None:
            ps.set_program_name(title)

        ps.init()
        ps.remove_all_structures()
        for k, v in self.state.items():
            v.register(ps)
        ps.show()

    def save(self, fname):
        np.savez_compressed(fname, state=self.state, allow_pickle=True)

    def load(self, fname):
        self.state = np.load(fname, allow_pickle=True)['state'].item()

    def __repr__(self):
        return f'PolyscopeObject({self.state})'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Please specify the visualization file you want to show')
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print('Specified file does not exist')
        sys.exit()

    object = PolyscopeObject(sys.argv[1])
    object.show(title=sys.argv[1].split('/')[-1])
