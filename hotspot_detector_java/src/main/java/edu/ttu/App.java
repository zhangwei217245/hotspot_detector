package edu.ttu;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.math3.ml.clustering.Cluster;
import org.apache.commons.math3.ml.clustering.Clusterable;
import org.apache.commons.math3.ml.clustering.DBSCANClusterer;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Hello world!
 */
public class App {

    static class MemRequest implements Clusterable {
        private int index;
        private long memaddress;

        public MemRequest(int index, long memaddress) {
            this.index = index;
            this.memaddress = memaddress;
        }

        public int getIndex() {
            return index;
        }

        public void setIndex(int index) {
            this.index = index;
        }

        public long getMemaddress() {
            return memaddress;
        }

        public void setMemaddress(long memaddress) {
            this.memaddress = memaddress;
        }

        public double[] getPoint() {
            return new double[]{this.index, this.memaddress};
        }
    }

    public static Collection<MemRequest> readMemRequest(String filepath) {
        final AtomicInteger i = new AtomicInteger(0);
        try(Stream<String> stream = Files.lines(Paths.get(filepath))) {
            return stream.map(line -> new MemRequest(i.incrementAndGet(), Long.decode(line.split(":")[3])))
                    .collect(Collectors.toList());
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }


    public static void main(String[] args) {

        String hex = "0x00000000FFFFFFFF";
        System.out.println(Long.decode(hex));

        if (args.length >= 3) {
            double eps = StringUtils.isBlank(args[0]) ? 2048.0 : Double.valueOf(args[0]);
            int minpts = StringUtils.isBlank(args[1]) ? 100 : Integer.valueOf(args[1]);

            String filePath = args[2];
            System.out.println(filePath);

            if (StringUtils.isBlank(filePath)) {
                System.err.println("The file path is not provided.");
                System.exit(0);
            }

            DBSCANClusterer<MemRequest> clusterer = new DBSCANClusterer<>(eps, minpts);

            List<Cluster<MemRequest>> cluster = clusterer.cluster(readMemRequest(filePath));

            cluster.forEach(c -> System.out.println(String.format("Cluster %d with size = %d",
                    c.hashCode(), c.getPoints().size())));

            System.out.println("Hello World!");
        }


    }
}
