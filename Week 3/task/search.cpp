#include "Search.h"

#include <queue>
#include <vector>
#include <cmath>

using namespace std;

struct State
{
    int x;
    int y;
    double g;
    double f;

    bool operator<(const State& other) const
    {
        return f > other.f;
    }
};

SearchResult astar(
    Graph& g,
    Node start,
    Node goal,
    function<double(Node,Node)> heuristic
)
{
    vector<vector<double>>
    dist(
        g.rows,
        vector<double>(
            g.cols,
            1e18
        )
    );

    priority_queue<State> pq;

    int explored = 0;

    dist[start.y][start.x] = 0;

    pq.push(
    {
        start.x,
        start.y,
        0,
        heuristic(start,goal)
    });

    while(!pq.empty())
    {
        auto cur = pq.top();
        pq.pop();

        if(cur.g >
           dist[cur.y][cur.x])
        {
            continue;
        }

        explored++;

        if(cur.x == goal.x &&
           cur.y == goal.y)
        {
            return {
                true,
                (int)cur.g,
                explored
            };
        }

        for(auto nxt :
            g.get_neighbors(
                {cur.x,cur.y}))
        {
            double ng =
                cur.g + 1;

            if(ng <
               dist[nxt.y]
                   [nxt.x])
            {
                dist[nxt.y]
                    [nxt.x]
                    = ng;

                double nf =
                    ng +
                    heuristic(
                        nxt,
                        goal
                    );

                pq.push(
                {
                    nxt.x,
                    nxt.y,
                    ng,
                    nf
                });
            }
        }
    }

    return {
        false,
        -1,
        explored
    };
}