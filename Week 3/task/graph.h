#pragma once
#include <vector>
#include <string>

struct Node {
    int x;
    int y;

    bool operator==(const Node& other) const {
        return x == other.x &&
               y == other.y;
    }
};

class Graph {
public:
    int rows;
    int cols;

    std::vector<std::vector<bool>> obstacle;

    Graph(std::string filename);

    std::vector<Node>
    get_neighbors(Node current);
};