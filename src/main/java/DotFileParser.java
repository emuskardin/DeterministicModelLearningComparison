import net.automatalib.alphabet.Alphabet;
import net.automatalib.alphabet.Alphabets;
import net.automatalib.automaton.transducer.MutableMealyMachine;
import net.automatalib.util.automaton.builder.AutomatonBuilders;
import net.automatalib.util.automaton.builder.MealyBuilder;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class DotFileParser {
    private final Path filePath;
    private final Alphabet<String> inputAlphabet;
    private final Alphabet<String> outputAlphabet;
    private final Alphabet<String> combinedAlphabet;
    private final MutableMealyMachine mealy;

    public DotFileParser(Path filePath) throws IOException {
        this.filePath = filePath;

        String data = new String(Files.readAllBytes(filePath));
        String digraph = data.substring(data.indexOf("{") + 1, data.lastIndexOf("}"));
        digraph = digraph.replaceAll("\\s",""); // remove whitespaces
        List<String> statements = Arrays.asList(digraph.split(";"));

        List<List<String>> transitions = new ArrayList<>();
        Set<String> inputAlphabetColl = new TreeSet<>();
        Set<String> outputAlphabetColl = new TreeSet<>();
        String initial = "";

        for (String stmt : statements) {
            if (stmt.contains("->")) {
                int label = stmt.indexOf("label=");
                if (label >= 0) {
                    int label_begin = stmt.indexOf("\"", label + 1);
                    int label_end = stmt.indexOf("\"", label_begin + 1);
                    int label_seperator = stmt.indexOf("/", label_begin + 1);
                    String from = stmt.substring(0, stmt.indexOf("->"));
                    String to = stmt.substring(stmt.indexOf("->") + 2, stmt.indexOf("["));
                    String input = stmt.substring(label_begin + 1, label_seperator);
                    String output = stmt.substring(label_seperator + 1, label_end);

                    inputAlphabetColl.add(input);
                    outputAlphabetColl.add(output);
                    transitions.add(Arrays.asList(from, input, output, to));
                } else if (stmt.contains("__start0")) {
                    initial = stmt.substring(stmt.indexOf("->") + 2);
                }
            }
        }

        if (initial.isEmpty()) {
            throw new RuntimeException("No initial state detected! Node __start0 not found!");
        }

        this.inputAlphabet = Alphabets.fromCollection(inputAlphabetColl);
        this.outputAlphabet = Alphabets.fromCollection(outputAlphabetColl);
        inputAlphabetColl.addAll(outputAlphabetColl);
        this.combinedAlphabet = Alphabets.fromCollection(inputAlphabetColl);


        MealyBuilder.MealyBuilder__4 builder = null;
        for (List<String> t : transitions) {
            if (builder == null) {
                builder = AutomatonBuilders.newMealy(inputAlphabet)
                        .from(t.get(0)).on(t.get(1)).withOutput(t.get(2)).to(t.get(3));

            } else {
                builder = builder.from(t.get(0)).on(t.get(1)).withOutput(t.get(2)).to(t.get(3));

            }
        }

        this.mealy = builder.withInitial(initial).create();
    }

    public Path getFilePath() {
        return filePath;
    }

    public Alphabet<String> getInputAlphabet() {
        return inputAlphabet;
    }

    public Alphabet<String> getOutputAlphabet() {
        return outputAlphabet;
    }

    public Alphabet<String> getCombinedAlphabet() {
        return combinedAlphabet;
    }

    public MutableMealyMachine getMealy() {
        return mealy;
    }
}
