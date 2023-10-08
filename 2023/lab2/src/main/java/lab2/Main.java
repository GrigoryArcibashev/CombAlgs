package lab2;

import lab2.common.Network;
import lab2.input.InputData;
import lab2.input.Reader;
import lab2.makers.MatrixMaker;
import lab2.makers.NetworkMaker;
import lab2.output.OutputData;
import lab2.output.Writer;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        InputData data = new Reader("src/main/resources/input.txt").readInput();
        Network network = NetworkMaker.make(data.capacities());
        FordFulkerson fordFulkerson = new FordFulkerson(network, data.s() - 1, data.t() - 1);
        int maxFlowValue = fordFulkerson.value();
        int[][] flowMatrix = MatrixMaker.make(network);
        new Writer("src/main/resources/output.txt").writeOutput(new OutputData(flowMatrix, maxFlowValue));
    }
}