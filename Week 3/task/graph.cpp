#include "Graph.h"
#include "json.hpp"
#include <fstream>

using json = nlohmann::json;
using namespace std;

Graph::Graph(string filename)
{
    ifstream file(filename);

    json j;
    file >> j;

    rows = j["grid_size"]["rows"];
    cols = j["grid_size"]["cols"];

    obstacle.resize(
        rows,
        vector<bool>(cols,false)
    );

    for(auto cell :
        j["obstacles"])
    {
        int y = cell["y"];
        int x = cell["x"];

        obstacle[y][x] = true;
    }
}

vector<Node>

Graph::get_neighbors(Node cur)
{
    vector<Node> ans;

    int dx[4] = {1,-1,0,0};
    int dy[4] = {0,0,1,-1};

    for(int i=0;i<4;i++)
    {
        int nx =
            cur.x + dx[i];

        int ny =
            cur.y + dy[i];

        if(nx < 0 ||
           nx >= cols)
            continue;

        if(ny < 0 ||
           ny >= rows)
            continue;

        if(obstacle[ny][nx])
            continue;

        ans.push_back(
            {nx,ny}
        );
    }

    return ans;
}