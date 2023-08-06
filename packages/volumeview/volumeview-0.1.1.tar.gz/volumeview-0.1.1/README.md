# volumeview

View 3D volumetric data, vector fields, and surfaces using figurl

## Installation

Volumeview uses [kachery](https://github.com/kacheryhub/kachery-doc/blob/main/README.md) and [figurl](https://github.com/magland/figurl/blob/main/README.md). To create figures, you must [set up a kachery node and run a kachery daemon](https://github.com/kacheryhub/kachery-doc/blob/main/doc/hostKacheryNode.md).

Install the latest version of volumeview:

```bash
pip install --upgrade volumeview
```

## 3D volume example

```python
import numpy as np
import volumeview as vv

a = np.zeros((2, 90, 60, 45), dtype=np.float32)
ix, iy, iz = np.meshgrid(*[np.linspace(-1, 1, n) for n in a.shape[1:]], indexing='ij')
a[0, :, :, :] = np.exp(-3 * (ix**2 + iy**2 + iz**2))
a[1, :, :, :] = np.ones(ix.shape) - 0.5 * (np.abs(ix) < 0.8) * (np.abs(iy) < 0.8) * (np.abs(iz) < 0.8)

F = vv.create_volume_view(a, component_names=['component 1', 'component 2'])
url = F.url(label='Test volume view')
print(url)
```

Produces: https://figurl.org/f?v=gs://figurl/volumeview-2&d=8e2d19eaa838930bc9e25dbc09afb7c6d719ede4&channel=flatiron1&label=Test%20volume%20view

## 3D vector field example

```python
import numpy as np
import volumeview as vv

a = np.zeros((3, 90, 60, 45), dtype=np.float32)
ix, iy, iz = np.meshgrid(*[np.linspace(-1, 1, n) for n in a.shape[1:]], indexing='ij')
a[0, :, :, :] = np.sin((ix + iy - iz) * 4 * np.pi) * np.exp(-3 * (ix**2 + iy**2 + iz**2))
a[1, :, :, :] = np.sin((iy + iz - ix) * 4 * np.pi) * np.exp(-3 * (ix**2 + iy**2 + iz**2))
a[2, :, :, :] = np.sin((ix + iz - iy) * 4 * np.pi) * np.exp(-3 * (ix**2 + iy**2 + iz**2))

F = vv.create_vector_field_view(a)
url = F.url(label='Test vector field view')
print(url)
```

Produces: https://figurl.org/f?v=gs://figurl/volumeview-2&d=48530916122545e6afeaf84645e7e13ea4651791&channel=flatiron1&label=Test%20vector%20field%20view

## Surface example

```python
import kachery_client as kc
import volumeview from vv

# your node needs to be a member of the flatiron1 kachery channel to obtain this file
vtk_uri = 'sha1://e54d59b5f12d226fdfe8a0de7d66a3efd1b83d69/rbc_001.vtk'
vtk_path = kc.load_file(vtk_uri)

vertices, faces = vv._parse_vtk_unstructured_grid(vtk_path)

# vertices is n x 3 array of vertex locations
# faces is m x 3 array of vertex indices for triangular mesh

F = vv.create_surface_view(vertices=vertices, faces=faces)
url = F.url(label='red blood cell')
print(url)
```

Produces: https://figurl.org/f?v=gs://figurl/volumeview-2&d=8cf32c552f9cb99aa3794b5c4976176b179c0009&channel=flatiron1&label=red%20blood%20cell