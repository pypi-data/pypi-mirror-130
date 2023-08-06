#pragma once
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/intersections.h>
#include <CGAL/Surface_mesh.h>
//#include <CGAL/Polygon_mesh_processing/orient_polygon_soup.h>
//#include <CGAL/Polygon_mesh_processing/polygon_soup_to_polygon_mesh.h>
#include <CGAL/Polygon_mesh_processing/compute_normal.h>
#include <CGAL/Polygon_mesh_processing/repair.h>
#include <CGAL/Polygon_mesh_processing/clip.h>
#include <boost/variant.hpp>
#include "glm/glm.hpp"
#include "types.hpp"

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Surface_mesh<K::Point_3> Mesh;

using TPolygon = vector<vector<tvec3>>;
using TPolygons = vector<vector<vector<tvec3>>>;
using TCGALFlatPolygon = vector<K::Point_3>;


inline K::Point_3 to_point3(const K::Point_2 &p)
{
    return K::Point_3(p.x(), p.y(), 0);
}

inline K::Point_3 to_point3(const tvec3 &v)
{
    return K::Point_3(v.x, v.y, v.z);
}

inline K::Point_2 to_point2(const tvec3 &v)
{
    return K::Point_2(v.x, v.y);
}

inline K::Triangle_3 to_triangle(const tvec3 triangle[3])
{
    return K::Triangle_3(to_point3(triangle[0]), to_point3(triangle[1]), to_point3(triangle[2]));
}

inline K::Triangle_2 to_triangle2(const tvec3 triangle[3])
{
    return K::Triangle_2(to_point2(triangle[0]), to_point2(triangle[1]), to_point2(triangle[2]));
}

inline tvec3 to_vec(const K::Point_3 &p)
{
    return tvec3(p.x(), p.y(), p.z());
}

inline tvec3 to_vec(const K::Point_2 &p)
{
    return tvec3(p.x(), p.y(), 0);
}

tfloat interpolate_z(const tvec3 triangle[3], const K::Line_3 & line);
