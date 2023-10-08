package lab2.input;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Reader {
    private final String path;

    public Reader(String pathToInputFile) {
        path = pathToInputFile;
    }

    public InputData readInput() throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        int N = Integer.parseInt(reader.readLine());
        int[][] capacities = readCapacities(reader, N);
        int s = Integer.parseInt(reader.readLine());
        int t = Integer.parseInt(reader.readLine());
        reader.close();
        return new InputData(N, s, t, capacities);
    }

    private int[][] readCapacities(BufferedReader reader, int N) throws IOException {
        List<int[]> capacities = new ArrayList<>();
        for (int i = 0; i < N; i += 1) {
            int[] line = Arrays
                    .stream(reader.readLine().split(" "))
                    .mapToInt(Integer::parseInt)
                    .toArray();
            capacities.add(line);
        }
        return capacities.toArray(new int[0][]);
    }
}
