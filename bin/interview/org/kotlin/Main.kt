fun main() {
    val inp = listOf(
        "prashant:om",
        "gary:prashant",
        "om:srini",
        "aaron:peter",
        "om:felix",
        "prashant:devon",
        "devon:aaron"
    )

    val e2m = mutableMapOf<String, String>()
    for (line in inp) {
        val (m, e) = line.split(":")
        e2m[e] = m
    }

    val orgs = mutableListOf<String>()
    for (e in e2m.keys) {
        var org = "/$e"
        var tempE = e
        while (e2m.containsKey(tempE)) {
            val m = e2m[tempE]!!
            org = "/$m$org"
            tempE = m
        }
        orgs.add(org)
    }

    orgs.sort()
    for (org in orgs) {
        println(org)
    }
}
