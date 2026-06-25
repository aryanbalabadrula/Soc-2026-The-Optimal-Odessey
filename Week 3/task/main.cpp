#include "json.hpp"
#include "Graph.h"
#include "Search.h"

#include <iostream>
#include <fstream>
#include <cmath>
#include <chrono>
#include <iomanip>

using namespace std;
using json = nlohmann::json;

int main()
{
    Graph g("graph.json");
    auto dijkstra =
    [](Node a, Node b)
    {
        return 0.0;
    };

    auto manhattan =
    [](Node a, Node b)
    {
        return (double)(
            abs(a.x - b.x)
            + abs(a.y - b.y)
        );
    };

    auto euclidean =
    [](Node a, Node b)
    {
        int dx = a.x - b.x;
        int dy = a.y - b.y;

        return sqrt(dx * dx + dy * dy);
    };

    ifstream qfile("queries.json");

    json queries;
    qfile >> queries;
    json output;
    output["meta"] = queries["meta"];
    output["results"] = json::array();
    for (auto e : queries["events"])
    {
        if (e["type"] != "find_path")
            continue;

        Node start =
        {
            e["start"]["x"],
            e["start"]["y"]
        };

        Node goal =
        {
            e["goal"]["x"],
            e["goal"]["y"]
        };
        auto t1 =
            chrono::high_resolution_clock::now();

        SearchResult d =
            astar(
                g,
                start,
                goal,
                dijkstra
            );

        auto t2 =
            chrono::high_resolution_clock::now();

        double d_ms =
            chrono::duration<
                double,
                std::milli
            >(t2 - t1).count();
        t1 =
            chrono::high_resolution_clock::now();

        SearchResult eu =
            astar(
                g,
                start,
                goal,
                euclidean
            );

        t2 =
            chrono::high_resolution_clock::now();

        double eu_ms =
            chrono::duration<
                double,
                std::milli
            >(t2 - t1).count();
        t1 =
            chrono::high_resolution_clock::now();

        SearchResult man =
            astar(
                g,
                start,
                goal,
                manhattan
            );

        t2 =
            chrono::high_resolution_clock::now();

        double man_ms =
            chrono::duration<
                double,
                std::milli
            >(t2 - t1).count();
        json ans;

        ans["id"] = e["id"];

        ans["dijkstra"] =
        {
            {"path_found", d.path_found},
            {"path_length", d.path_length},
            {"nodes_explored", d.nodes_explored},
            {"time_ms", d_ms}
        };

        ans["astar_euclidean"] =
        {
            {"path_found", eu.path_found},
            {"path_length", eu.path_length},
            {"nodes_explored", eu.nodes_explored},
            {"time_ms", eu_ms}
        };

        ans["astar_manhattan"] =
        {
            {"path_found", man.path_found},
            {"path_length", man.path_length},
            {"nodes_explored", man.nodes_explored},
            {"time_ms", man_ms}
        };

        output["results"].push_back(ans);
    }

    ofstream out("output.json");

    out << setw(4) << output;

    return 0;
}   