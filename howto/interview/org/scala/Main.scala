object Main extends App {
    val inp = List(
        "prashant:om",
        "gary:prashant",
        "om:srini",
        "aaron:peter",
        "om:felix",
        "prashant:devon",
        "devon:aaron"
    )

    var e2m = Map[String, String]()
    for (line <- inp) {
        val splitLine = line.split(":")
        val m = splitLine(0)
        val e = splitLine(1)
        e2m += (e -> m)
    }

    var orgs = List[String]()
    for (e <- e2m.keys) {
        var org = "/" + e
        var tempE = e
        while (e2m.contains(tempE)) {
            val m = e2m(tempE)
            org = "/" + m + org
            tempE = m
        }
        orgs = org :: orgs
    }

    orgs = orgs.sorted
    for (org <- orgs) {
        println(org)
    }
}
