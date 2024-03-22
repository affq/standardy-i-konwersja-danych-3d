import open3d
import numpy as np
import shapely

# open3d.geometry
# open3d.visualization
# open3d.utility

def draw_mesh():
    mesh: open3d.geometry.TriangleMesh = open3d.geometry.TriangleMesh.create_sphere()
    mesh.compute_vertex_normals()

    open3d.visualization.draw_geometries(
        [mesh]
    )

def save_mesh():
    mesh: open3d.geometry.TriangleMesh = open3d.geometry.TriangleMesh.create_sphere()
    mesh.compute_vertex_normals()

    open3d.io.write_triangle_mesh("mesh.ply", mesh)


if __name__ == '__main__':
    polygon = shapely.Polygon.from_bounds(0.0, 0.0, 10.0, 30.0)
    min_height = 0.0
    max_height = 60.0

    xy = polygon.exterior.coords
    xy = list(xy[:-1])
    xy = np.float64(xy)
    
    xyz_min = np.hstack([
        xy, np.full(xy.shape[0], min_height)[:, np.newaxis]
    ])

    xyz_max = np.hstack([
        xy, np.full(xy.shape[0], max_height)[:, np.newaxis]
    ])

    xyz = np.vstack([
        xyz_min,
        xyz_max
    ])

    num_vertices_base = xy.shape[0]
    triangles = []
    for i in range(xy.shape[0] - 1):
        triangles.append(
            [i, i + 1, i + 1 + num_vertices_base]
        )
        triangles.append(
            [i + 1 + num_vertices_base, i + num_vertices_base, i]
        )
    triangles.append([num_vertices_base - 1, 0, num_vertices_base])
    triangles.append([num_vertices_base, num_vertices_base + num_vertices_base, 0])
    
    mesh = open3d.geometry.TriangleMesh(
        open3d.utility.Vector3dVector(xyz),
        open3d.utility.Vector3iVector(triangles)
    )

    open3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

    print(xyz)