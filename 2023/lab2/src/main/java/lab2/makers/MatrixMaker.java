package lab2.makers;

import lab2.common.Edge;
import lab2.common.Network;

public class MatrixMaker {
    public static int[][] make(Network network) {
        int N = network.vertexCount();
        int[][] matrix = new int[N][N];
        for (Edge edge : network.edges())
            matrix[edge.from()][edge.to()] = (int) Math.round(edge.flow());
        return matrix;
    }
}
