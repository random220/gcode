use std::collections::HashMap;

fn main() {
    let input = vec![
        "prashant:om",
        "gary:prashant",
        "om:srini",
        "aaron:peter",
        "om:felix",
        "prashant:devon",
        "devon:aaron",
    ];

    let mut e2m: HashMap<&str, &str> = HashMap::new();
    for line in &input {
        let parts: Vec<&str> = line.split(':').collect();
        let m = parts[0];
        let e = parts[1];
        e2m.insert(e, m);
    }

    let mut orgs: Vec<String> = Vec::new();
    for &e in e2m.keys() {
        let mut org = format!("/{}", e);
        let mut curr = e;
        while let Some(&m) = e2m.get(curr) {
            org = format!("/{}{}", m, org);
            curr = m;
        }
        orgs.push(org);
    }

    orgs.sort();
    for org in orgs {
        println!("{}", org);
    }
}
