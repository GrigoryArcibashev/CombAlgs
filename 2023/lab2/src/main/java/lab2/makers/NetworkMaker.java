package lab2.makers;

import lab2.common.Edge;
import lab2.common.Network;

public class NetworkMaker {
    public static Network make(int[][] capacities) {
        int N = capacities.length;
        Network network = new Network(N);
        for (int v = 0; v < N; v++)
            for (int w = 0; w < N; w++)
                if (capacities[v][w] > 0)
                    network.addEdge(new Edge(v, w, capacities[v][w]));
        return network;
    }
}