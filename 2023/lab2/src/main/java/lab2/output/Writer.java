package lab2.output;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

public class Writer {
    private final String path;

    public Writer(String pathToOutputFile) {
        path = pathToOutputFile;
    }

    public void writeOutput(OutputData output) throws IOException {
        FileWriter writer = new FileWriter(path);
        writeFlows(writer, output.flows());
        writer.write(output.maxFlowValue() + "\n");
        writer.flush();
    }

    private void writeFlows(FileWriter writer, int[][] flows) throws IOException {
        for (int[] line : flows) {
            String writeLine = String.join(" ", Arrays.stream(line).mapToObj(String::valueOf).toList());
            writer.write(writeLine + "\n");
        }
    }
}
