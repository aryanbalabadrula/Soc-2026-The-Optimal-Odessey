#include <functional>
#pragma once
#include "Graph.h"

struct SearchResult
{
    bool path_found;
    int path_length;
    int nodes_explored;
};

SearchResult astar(
    Graph& g,
    Node start,
    Node goal,
    std::function<double(Node,Node)> heuristic
);

