import java.util.*;

public class Main {
    public static void main(String[] args) {
        String[] inp = {
            "prashant:om",
            "gary:prashant",
            "om:srini",
            "aaron:peter",
            "om:felix",
            "prashant:devon",
            "devon:aaron",
        };

        Map<String, String> e2m = new HashMap<>();
        for(String line : inp) {
            String[] splitLine = line.split(":");
            String m = splitLine[0];
            String e = splitLine[1];
            e2m.put(e, m);
        }

        List<String> orgs = new ArrayList<>();
        for(String e : e2m.keySet()) {
            String org = "/" + e;
            while(e2m.containsKey(e)) {
                String m = e2m.get(e);
                org = "/" + m + org;
                e = m;
            }
            orgs.add(org);
        }

        Collections.sort(orgs);
        for(String org : orgs) {
            System.out.println(org);
        }
    }
}
