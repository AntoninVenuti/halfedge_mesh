import halfedge_mesh
import pytest
import math
import numpy as np

class TestHalfedgeMesh:
#                               Data
#------------------------------------------------------------------------------
    @pytest.fixture()
    def cube_off_mesh(self):
        return halfedge_mesh.HalfedgeMesh("tests/data/cube.off")

    @pytest.fixture()
    def cube_large_off_mesh(self):
        return halfedge_mesh.HalfedgeMesh("tests/data/cube_large.off")

    @pytest.fixture()
    def cube_negative_off_mesh(self):
        return halfedge_mesh.HalfedgeMesh("tests/data/cube4.off")
#------------------------------------------------------------------------------
    def test_eq_halfedge_mesh_cube(self, cube_off_mesh, cube_large_off_mesh):
        assert cube_off_mesh != cube_large_off_mesh
        assert cube_off_mesh == cube_off_mesh

    def test_hash_halfedge_mesh_cube(self, cube_off_mesh):
        constant_value = 10111970
        test_dic = dict()
        test_dic[cube_off_mesh] = constant_value
        assert test_dic[cube_off_mesh] == constant_value

    def discard_comments(self, cube_off_mesh):
        with open("tests/data/cube_comments.off") as comments:
            assert cube_off_mesh.discard_comments(comments, "#") == "OFF"

    def test_read_file(self, cube_off_mesh):
        assert cube_off_mesh.read_file("tests/data/cube.off") != None
        assert cube_off_mesh.read_file("") == None
        assert cube_off_mesh.read_file("tests/data/cube.ply") == None
        assert cube_off_mesh.read_file("tests/data/cube_comments.off") != None

    def test_read_off_vertices(self, cube_off_mesh):
        with open("tests/data/vertices_test.off") as vertices:
            v = cube_off_mesh.read_off_vertices(vertices, 2)
            assert np.allclose([v[0].x(), v[0].y(), v[0].z()], [10.3, 42., 20.])
            assert np.allclose([v[1].x(), v[1].y(), v[1].z()], [33, 21.3, 94.1])

    def test_parse_build_halfedge_off(self, cube_off_mesh):
        with open("tests/data/faces_test.off") as faces:
            vertices = [halfedge_mesh.Vertex(-1,-1,-1,i) for i in range(3)]
            f, e = cube_off_mesh.parse_build_halfedge_off(faces, 1, vertices)
            assert len(f) == 1
            assert f[0].a == 0 and f[0].b == 1 and f[0].c == 2
            assert f[0].index == 0
            assert len(e) == 3

    def test_update_vertices(self, cube_off_mesh):

        new_vertices = [[10, -10, -10],
                        [10, -10, 10],
                        [-10, -10, 10],
						[-10, -10, -10],
						[10, 10, -10],
						[10, 10, 10],
						[-10, 10, 10],
						[-10, 10, -10]]

        cube_off_mesh.update_vertices(new_vertices)

        for k, i in enumerate(cube_off_mesh.vertex_list):
            assert new_vertices[k][0] == i.x()
            assert new_vertices[k][1] == i.y()
            assert new_vertices[k][2] == i.z()

    def test_halfedge_loop_around_facet(self, cube_off_mesh):
        halfedge = cube_off_mesh.facet_list[0].halfedge()
        assert halfedge.next().next().next().vertex() == halfedge.vertex()

    def test_vertices_in_facet(self, cube_off_mesh):
        halfedge = cube_off_mesh.facet_list[0].halfedge()

        # make sure all vertices are in the facet described by halfedge
        assert np.allclose(halfedge.vertex().coordinates, np.array([1.,-1.,1.]))

        assert np.allclose(halfedge.next().vertex().coordinates,
            np.array([-1,-1,1]))

        assert np.allclose(halfedge.next().next().vertex().coordinates,
            np.array([1,-1,-1]))

    def test_facet_eq_correct_for_same_object_and_diff_objects(self,
                                                               cube_off_mesh):
        assert cube_off_mesh.facet_list[0] == cube_off_mesh.facet_list[0]
        assert cube_off_mesh.facet_list[1] != cube_off_mesh.facet_list[0]

        assert cube_off_mesh.facet_list[3] == cube_off_mesh.facet_list[3]
        assert cube_off_mesh.facet_list[0] != cube_off_mesh.facet_list[3]

    def test_halfedgemesh_vertices_are_in_order_with_cubeoff(self,
                                                             cube_off_mesh):
        # Tests parse_off since Vertex is just a basic class
        vertices = cube_off_mesh.vertex_list

        # cube vertices in order
        pts = [1, -1, -1,
               1, -1, 1,
               -1, -1, 1,
               -1, -1, -1,
               1, 1, -0.999999,
               0.999999, 1, 1.000001]

        count = 0
        for index in range(0, len(vertices), 3):
            np.allclose(vertices[count].coordinates,
                        [pts[index], pts[index+1],pts[index+2]])
            count += 1

    def test_halfedgemesh_vertices_in_facet_exists_with_cubeoff(self,
                                                                cube_off_mesh):
        # Tests parse_off since Vertex is just a basic class

        facets = cube_off_mesh.facet_list
        vertices = cube_off_mesh.vertex_list

        for index in range(len(facets)):
            # check that it's within the range of the number of vertices
            assert facets[index].a < len(vertices)
            assert (facets[index].a >= 0)


    #def test_halfedgemesh_get_halfedge_returns_correct_vertices_with_cubeoff(
    #        self, cube_off_mesh):

    #    five_seven = cube_off_mesh.get_halfedge(5, 7)
    #    assert five_seven.vertex.index == 7
    #    assert five_seven.prev.vertex.index == 5

    #    five_six = cube_off_mesh.get_halfedge(5, 6)
    #    assert five_six.vertex.index == 6
    #    assert five_six.prev.vertex.index == 5

    #    one_two = cube_off_mesh.get_halfedge(1, 2)
    #    assert one_two.vertex.index == 2
    #    assert one_two.prev.vertex.index == 1

#------------------------------------------------------------------------------
 # TODO: Check connectivity after update vertices

    #def test_halfedge_opposite_correct_vertices_with_cubeoff(self,
    #                                                         cube_off_mesh):

    #    zero_two = cube_off_mesh.get_halfedge(0, 2)
    #    assert zero_two.opposite.vertex.index == 0
    #    assert zero_two.opposite.prev.vertex.index == 2

    #    zero_one = cube_off_mesh.get_halfedge(0, 1)
    #    assert zero_one.opposite.vertex.index == 0
    #    assert zero_one.opposite.prev.vertex.index == 1

    #    four_one = cube_off_mesh.get_halfedge(4, 1)
    #    assert four_one.opposite.vertex.index == 4
    #    assert four_one.opposite.prev.vertex.index == 1

    #def test_halfedge_eq_correct_for_same_and_object_and_diff_objects(self,
    #                                                                  cube_off_mesh):

    #    zero_two = cube_off_mesh.get_halfedge(0, 2)
    #    assert zero_two == zero_two

    #    four_one = cube_off_mesh.get_halfedge(4, 1)
    #    assert zero_two != four_one

    ## test negative angles
    def test_get_angle_normal(self, cube_off_mesh, cube_negative_off_mesh):

        assert cube_off_mesh.facet_list[0].halfedge().vertex().index == 1
        assert cube_off_mesh.facet_list[0].halfedge().prev().vertex().index == 0

        assert np.allclose(
                cube_off_mesh.facet_list[0].halfedge().angle_normal(),
                    math.pi/2.0)

        assert cube_off_mesh.facet_list[1].halfedge().vertex().index == 7
        assert cube_off_mesh.facet_list[1].halfedge().prev().vertex().index == 4
        assert np.allclose(
                cube_off_mesh.facet_list[1].halfedge().angle_normal(),
                math.pi/2.0)

        assert cube_off_mesh.facet_list[3].halfedge().next().vertex().index == 2
        assert cube_off_mesh.facet_list[3].halfedge().next().prev().vertex().index == 5
        assert np.allclose(
                cube_off_mesh.facet_list[3].halfedge().next().angle_normal(), 0.0)

    def test_get_vertex(self, cube_off_mesh):
        mesh_vertex = cube_off_mesh.vertex_list[0].coordinates
        test_vertex = [1,-1,-1]
        assert np.allclose(mesh_vertex, test_vertex)

    def test_update_vertices(self, cube_off_mesh, cube_large_off_mesh):
        tmp = halfedge_mesh.HalfedgeMesh()
        tmp.vertex_list = cube_off_mesh.vertex_list[:]
        tmp.halfedge_list = cube_off_mesh.halfedge_list[:]
        tmp.facet_list = cube_off_mesh.facet_list[:]

        v = []
        for vertex in cube_large_off_mesh.vertex_list:
           v.append([ vertex.x(), vertex.y(), vertex.z() ])

        tmp.update_vertices(v)

        for i in range(len(cube_large_off_mesh.halfedge_list)):
            tmp_angle = tmp.halfedge_list[i].angle_normal()
            cube_angle = cube_large_off_mesh.halfedge_list[i].angle_normal()
            assert tmp_angle == cube_angle
