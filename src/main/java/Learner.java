import de.learnlib.algorithm.LearningAlgorithm;
import de.learnlib.algorithm.kv.mealy.KearnsVaziraniMealy;
import de.learnlib.algorithm.lstar.ce.ObservationTableCEXHandlers;
import de.learnlib.algorithm.lstar.closing.ClosingStrategies;
import de.learnlib.algorithm.lstar.mealy.ExtensibleLStarMealy;
import de.learnlib.algorithm.ttt.mealy.TTTLearnerMealy;
import de.learnlib.driver.simulator.MealySimulatorSUL;
import de.learnlib.filter.cache.sul.SULCaches;
import de.learnlib.filter.statistic.Counter;
import de.learnlib.filter.statistic.sul.ResetCounterSUL;
import de.learnlib.filter.statistic.sul.SymbolCounterSUL;
import de.learnlib.oracle.EquivalenceOracle;
import de.learnlib.oracle.equivalence.MealyRandomWordsEQOracle;
import de.learnlib.oracle.membership.MealySimulatorOracle;
import de.learnlib.oracle.membership.SULOracle;
import de.learnlib.statistic.StatisticSUL;
import de.learnlib.sul.SUL;
import de.learnlib.util.Experiment;
import de.learnlib.util.statistic.SimpleProfiler;
import net.automatalib.alphabet.Alphabet;
import net.automatalib.alphabet.ListAlphabet;
import net.automatalib.automaton.transducer.CompactMealy;
import net.automatalib.automaton.transducer.MealyMachine;
import net.automatalib.serialization.dot.GraphDOT;
import net.automatalib.util.automaton.random.RandomAutomata;
import net.automatalib.word.Word;

import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import static de.learnlib.acex.AcexAnalyzers.BINARY_SEARCH_BWD;

public class Learner {

    public static void increase_mealy_size() throws IOException {

        int numIncreases = 20;
        int repeat = 1;
        int numStates = 100;

        List<Integer> inputs = new ArrayList<>(Arrays.asList(0, 1, 2, 3, 4));
        List<Integer> outputs = new ArrayList<>(Arrays.asList(0, 1, 2, 3, 4));

        Alphabet<Integer> alphabet = new ListAlphabet<>(inputs);
        Alphabet<Integer> outputAlphabet =  new ListAlphabet<>(outputs);

        List<Word<Integer>> initialSuffixes = new ArrayList<>();
        alphabet.forEach(it -> {initialSuffixes.add(Word.fromSymbols(it));});

        List<Double> all_times_ls = new ArrayList<>();
        List<Double> all_queries_ls = new ArrayList<>();
        List<Double> all_steps_ls = new ArrayList<>();

        List<Double> all_times_kv = new ArrayList<>();
        List<Double> all_queries_kv = new ArrayList<>();
        List<Double> all_steps_kv = new ArrayList<>();

        List<Double> all_times_ttt = new ArrayList<>();
        List<Double> all_queries_ttt = new ArrayList<>();
        List<Double> all_steps_ttt = new ArrayList<>();

        ArrayList<String> algs = new ArrayList<>();
        algs.add("LS");
        algs.add("KV");
        algs.add("TTT");

        for (int j = 0; j < numIncreases; j++) {
            List<Double> times_ls = new ArrayList<>();
            List<Double> queries_ls = new ArrayList<>();
            List<Double> steps_ls = new ArrayList<>();

            List<Double> times_kv = new ArrayList<>();
            List<Double> queries_kv = new ArrayList<>();
            List<Double> steps_kv = new ArrayList<>();

            List<Double> times_ttt = new ArrayList<>();
            List<Double> queries_ttt = new ArrayList<>();
            List<Double> steps_ttt = new ArrayList<>();

            for (int i = 0; i < repeat; i++) {

                CompactMealy<Integer, Integer> target = RandomAutomata.randomMealy(new Random(), numStates, alphabet, outputAlphabet, true);

                FileWriter fw = new FileWriter("models/stateIncrease/Mealy_" + j + "_states_" + i +".txt");
                final StringWriter writer = new StringWriter();

                GraphDOT.write(target, alphabet, writer);
                fw.write(writer.toString());
                fw.close();

                for (String alg : algs ) {

                    MealySimulatorSUL<Integer, Integer> driver = new MealySimulatorSUL<>(target);

                    StatisticSUL<Integer, Integer> queryStatisticSul = new ResetCounterSUL<>("membership queries", driver);
                    StatisticSUL<Integer, Integer> stepStatisticSul = new SymbolCounterSUL<>("steps", queryStatisticSul);

                    SUL<Integer, Integer> effectiveSul = stepStatisticSul;
                    effectiveSul = SULCaches.createCache(alphabet, effectiveSul);

                    SULOracle<Integer, Integer> mqOracle = new SULOracle<>(effectiveSul);
                    LearningAlgorithm<? extends MealyMachine<?, Integer, ?, Integer>, Integer, Word<Integer>> learningAlg = null;

                    if (alg.equals("LS")) {
                        learningAlg = new ExtensibleLStarMealy<>(alphabet, mqOracle, initialSuffixes, ObservationTableCEXHandlers.RIVEST_SCHAPIRE, ClosingStrategies.CLOSE_SHORTEST);
                    }
                    if (alg.equals("KV")) {
                        learningAlg = new KearnsVaziraniMealy<>(alphabet, mqOracle, true, BINARY_SEARCH_BWD);
                    }
                    if (alg.equals("TTT")) {
                        learningAlg = new TTTLearnerMealy<>(alphabet, mqOracle, BINARY_SEARCH_BWD);
                    }

                    EquivalenceOracle.MealyEquivalenceOracle<Integer, Integer> eqOracle = new MealyRandomWordsEQOracle<Integer, Integer>(
                            new MealySimulatorOracle<>(target),
                            10,
                            50,
                            10000,
                            new Random() // make results reproducible
                    );

                    Experiment.MealyExperiment<Integer, Integer> experiment = new Experiment.MealyExperiment<>(learningAlg, eqOracle, alphabet);
                    experiment.setProfile(true);
                    experiment.setLogModels(true);
                    SimpleProfiler.reset();

                    experiment.run();

                    Counter e = SimpleProfiler.cumulated("Learning");

                    assert e != null;
                    long learning_time = e.getCount();

                    SimpleProfiler.logResults();

                    MealyMachine<?, Integer, ?, Integer> result = experiment.getFinalHypothesis();
                    // model statistics
                    if (result.size() != target.size())
                        System.out.println("Learning failed." + result.size() + " vs " + numStates);

                    if (alg.equals("LS")) {
                        times_ls.add((double) learning_time / 1000);
                        steps_ls.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_ls.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }
                    if (alg.equals("KV")) {
                        times_kv.add((double) learning_time / 1000);
                        steps_kv.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_kv.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }
                    if (alg.equals("TTT")) {
                        times_ttt.add((double) learning_time / 1000);
                        steps_ttt.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_ttt.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }

                }
            }

            all_times_ls.add(times_ls.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_ls.add(queries_ls.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_ls.add(steps_ls.stream().mapToDouble(val -> val).average().orElse(0.0));

            all_times_kv.add(times_kv.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_kv.add(queries_kv.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_kv.add(steps_kv.stream().mapToDouble(val -> val).average().orElse(0.0));

            all_times_ttt.add(times_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_ttt.add(queries_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_ttt.add(steps_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));


            numStates += 100;
        }

        System.out.println("LS (Time, Queries, Steps)");
        System.out.println(all_times_ls);
        System.out.println(all_queries_ls);
        System.out.println(all_steps_ls);

        System.out.println("KV (Time, Queries, Steps)");
        System.out.println(all_times_kv);
        System.out.println(all_queries_kv);
        System.out.println(all_steps_kv);

        System.out.println("TTT (Time, Queries, Steps)");
        System.out.println(all_times_ttt);
        System.out.println(all_queries_ttt);
        System.out.println(all_steps_ttt);
    }

    public static void increase_mealy_alphabet() throws IOException {

        int alphSize = 10;
        int numIncreases = 10;
        int repeat = 10;
        int numStates = 200;

        List<Double> all_times_ls = new ArrayList<>();
        List<Double> all_queries_ls = new ArrayList<>();
        List<Double> all_steps_ls = new ArrayList<>();

        List<Double> all_times_kv = new ArrayList<>();
        List<Double> all_queries_kv = new ArrayList<>();
        List<Double> all_steps_kv = new ArrayList<>();

        List<Double> all_times_ttt = new ArrayList<>();
        List<Double> all_queries_ttt = new ArrayList<>();
        List<Double> all_steps_ttt = new ArrayList<>();

        ArrayList<String> algs = new ArrayList<>();
        algs.add("LS");
        algs.add("KV");
        algs.add("TTT");

        for (int j = 0; j < numIncreases; j++) {
            List<Double> times_ls = new ArrayList<>();
            List<Double> queries_ls = new ArrayList<>();
            List<Double> steps_ls = new ArrayList<>();

            List<Double> times_kv = new ArrayList<>();
            List<Double> queries_kv = new ArrayList<>();
            List<Double> steps_kv = new ArrayList<>();

            List<Double> times_ttt = new ArrayList<>();
            List<Double> queries_ttt = new ArrayList<>();
            List<Double> steps_ttt = new ArrayList<>();

            List<Integer> outputs = new ArrayList<>(Arrays.asList(0, 1, 2, 3, 4));
            List<Integer> inputs = new ArrayList<Integer>();
            for (int re = 0; re < alphSize; re++) {
                inputs.add(re);
            }

            Alphabet<Integer> alphabet = new ListAlphabet<Integer>(inputs);
            Alphabet<Integer> outputAlphabet = new ListAlphabet<>(outputs);
            // instantiate test driver

            List<Word<Integer>> initialSuffixes = new ArrayList<>();
            alphabet.forEach(it -> {
                initialSuffixes.add(Word.fromSymbols(it));
            });

            for (int i = 0; i < repeat; i++) {

                CompactMealy<Integer, Integer> target = RandomAutomata.randomMealy(new Random(), numStates, alphabet, outputAlphabet, true);

                FileWriter fw = new FileWriter("models/alphIncrease/Mealy_" + j + "_alph_size_" + i +".txt");
                final StringWriter writer = new StringWriter();

                GraphDOT.write(target, alphabet, writer);
                fw.write(writer.toString());
                fw.close();

                for (String alg : algs ) {

                    MealySimulatorSUL<Integer, Integer> driver = new MealySimulatorSUL<>(target);

                    StatisticSUL<Integer, Integer> queryStatisticSul = new ResetCounterSUL<>("membership queries", driver);
                    StatisticSUL<Integer, Integer> stepStatisticSul = new SymbolCounterSUL<>("steps", queryStatisticSul);

                    SUL<Integer, Integer> effectiveSul = stepStatisticSul;
                    effectiveSul = SULCaches.createCache(alphabet, effectiveSul);

                    SULOracle<Integer, Integer> mqOracle = new SULOracle<>(effectiveSul);
                    LearningAlgorithm<? extends MealyMachine<?, Integer, ?, Integer>, Integer, Word<Integer>> learningAlg = null;

                    if (alg.equals("LS")) {
                        learningAlg = new ExtensibleLStarMealy<>(alphabet, mqOracle, initialSuffixes, ObservationTableCEXHandlers.RIVEST_SCHAPIRE, ClosingStrategies.CLOSE_SHORTEST);
                    }
                    if (alg.equals("KV")) {
                        learningAlg = new KearnsVaziraniMealy<>(alphabet, mqOracle, true, BINARY_SEARCH_BWD);
                    }
                    if (alg.equals("TTT")) {
                        learningAlg = new TTTLearnerMealy<>(alphabet, mqOracle, BINARY_SEARCH_BWD);
                    }

                    EquivalenceOracle.MealyEquivalenceOracle<Integer, Integer> eqOracle = new MealyRandomWordsEQOracle<Integer, Integer>(
                            new MealySimulatorOracle<>(target),
                            10,
                            50,
                            10000,
                            new Random() // make results reproducible
                    );

                    Experiment.MealyExperiment<Integer, Integer> experiment = new Experiment.MealyExperiment<>(learningAlg, eqOracle, alphabet);
                    experiment.setProfile(true);
                    experiment.setLogModels(true);
                    SimpleProfiler.reset();

                    experiment.run();

                    Counter e = SimpleProfiler.cumulated("Learning");

                    assert e != null;
                    long learning_time = e.getCount();

                    SimpleProfiler.logResults();

                    MealyMachine<?, Integer, ?, Integer> result = experiment.getFinalHypothesis();
                    // model statistics
                    if (result.size() != target.size())
                        System.out.println("Learning failed." + result.size() + " vs " + numStates);

                    if (alg.equals("LS")) {
                        times_ls.add((double) learning_time / 1000);
                        steps_ls.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_ls.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }
                    if (alg.equals("KV")) {
                        times_kv.add((double) learning_time / 1000);
                        steps_kv.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_kv.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }
                    if (alg.equals("TTT")) {
                        times_ttt.add((double) learning_time / 1000);
                        steps_ttt.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                        queries_ttt.add(Double.parseDouble(queryStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                    }

                }
            }

            all_times_ls.add(times_ls.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_ls.add(queries_ls.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_ls.add(steps_ls.stream().mapToDouble(val -> val).average().orElse(0.0));

            all_times_kv.add(times_kv.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_kv.add(queries_kv.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_kv.add(steps_kv.stream().mapToDouble(val -> val).average().orElse(0.0));

            all_times_ttt.add(times_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_queries_ttt.add(queries_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));
            all_steps_ttt.add(steps_ttt.stream().mapToDouble(val -> val).average().orElse(0.0));


            alphSize += 10;
        }

        System.out.println("LS (Time, Queries, Steps)");
        System.out.println(all_times_ls);
        System.out.println(all_queries_ls);
        System.out.println(all_steps_ls);

        System.out.println("KV (Time, Queries, Steps)");
        System.out.println(all_times_kv);
        System.out.println(all_queries_kv);
        System.out.println(all_steps_kv);

        System.out.println("TTT (Time, Queries, Steps)");
        System.out.println(all_times_ttt);
        System.out.println(all_queries_ttt);
        System.out.println(all_steps_ttt);
    }

    public static void realWorldBenchmarks() throws IOException{

        int numRepeats = 10;

        ArrayList<String> algs = new ArrayList<>();
        algs.add("LS");
        algs.add("KV");
        algs.add("TTT");

        DotFileParser tcp3 = new DotFileParser(Paths.get("models/realWorldExamples/tcp_client_ubuntu.dot"));

        DotFileParser mqtt = new DotFileParser(Paths.get("models/realWorldExamples/VerneMQ__two_client_will_retain.dot"));
        DotFileParser mqtt2 = new DotFileParser(Paths.get("models/realWorldExamples/mosquitto__two_client_will_retain.dot"));

        DotFileParser login = new DotFileParser(Paths.get("models/realWorldExamples/ABP_Channel_Frame.flat_0_10.dot"));

        List<DotFileParser> allModels = Arrays.asList(tcp3, mqtt, mqtt2, login);

        for (DotFileParser dotModel : allModels){
            System.out.println(dotModel.getFilePath().toString());
            for (String alg : algs ) {

                System.out.println(alg + " times/steps");
                List<Double> times = new ArrayList<>();
                List<Double> steps = new ArrayList<>();

                for (int i = 0; i < numRepeats; i++) {

                    Alphabet<String> inputs = dotModel.getInputAlphabet();

                    List<Word<String>> initialSuffixes = new ArrayList<>();
                    inputs.forEach(it -> {
                        initialSuffixes.add(Word.fromSymbols(it));
                    });

                    MealySimulatorSUL<String, String> sul = new MealySimulatorSUL<String, String>(dotModel.getMealy());
                    StatisticSUL<String, String> queryStatisticSul = new ResetCounterSUL<String, String>("membership queries", sul);
                    StatisticSUL<String, String> stepStatisticSul = new SymbolCounterSUL<>("steps", queryStatisticSul);

                    SUL<String, String> effectiveSul = stepStatisticSul;
                    effectiveSul = SULCaches.createCache(inputs, effectiveSul);

                    SULOracle<String, String> mqOracle = new SULOracle<>(effectiveSul);
                    LearningAlgorithm<? extends MealyMachine<?, String, ?, String>, String, Word<String>> learningAlg = null;

                    if (alg.equals("LS")) {
                        learningAlg = new ExtensibleLStarMealy<>(inputs, mqOracle, initialSuffixes, ObservationTableCEXHandlers.RIVEST_SCHAPIRE, ClosingStrategies.CLOSE_SHORTEST);
                    }
                    if (alg.equals("KV")) {
                        learningAlg = new KearnsVaziraniMealy<>(inputs, mqOracle, true, BINARY_SEARCH_BWD);
                    }
                    if (alg.equals("TTT")) {
                        learningAlg = new TTTLearnerMealy<>(inputs, mqOracle, BINARY_SEARCH_BWD);
                    }

                    EquivalenceOracle.MealyEquivalenceOracle<String, String> eqOracle = new MealyRandomWordsEQOracle<>(
                            new MealySimulatorOracle<>(dotModel.getMealy()),
                            10,
                            50,
                            20000
                    );


                    Experiment.MealyExperiment<String, String> experiment = new Experiment.MealyExperiment<>(learningAlg, eqOracle, inputs);
                    experiment.setProfile(true);
                    experiment.setLogModels(true);
                    SimpleProfiler.reset();

                    experiment.run();

                    Counter e = SimpleProfiler.cumulated("Learning");

                    assert e != null;
                    long learning_time = e.getCount();
                    SimpleProfiler.logResults();

                    MealyMachine<?, String, ?, String> result = experiment.getFinalHypothesis();
                    // model statistics
                    if (result.size() != dotModel.getMealy().size())
                        System.out.println("Learning failed.");

                    times.add((double) learning_time / 1000);
                    steps.add(Double.parseDouble(stepStatisticSul.getStatisticalData().getDetails().split(": ")[1]));
                }

                System.out.println(times.stream().mapToDouble(val -> val).average().orElse(0.0));
                System.out.println(steps.stream().mapToDouble(val -> val).average().orElse(0.0));
            }
        }

    }

    public static void main(String[] args) throws IOException, InterruptedException, NoSuchMethodException {
        System.out.println("Mealy Size Increase");
        increase_mealy_size();
        System.out.println("Mealy Alphabet Increase");
        increase_mealy_alphabet();
        System.out.println("Real World Benchmark Models");
        realWorldBenchmarks();
    }
}

